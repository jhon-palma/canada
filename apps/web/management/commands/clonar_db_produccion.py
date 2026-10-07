"""Trae una copia de la base de produccion y la deja montada en local.

Desarrollar contra una base vacia esconde la mitad de los problemas. Las
fichas reales traen campos a medias, barrios con tildes, articulos con HTML
pegado de Word y 392 propiedades donde el entorno limpio tiene tres; cosas que
solo aparecen cuando los datos son los de verdad. Este comando hace el viaje
completo: vuelca produccion, borra el esquema local y restaura encima.

Se apoya en pg_dump y pg_restore en vez de en los volcados de Django porque
`dumpdata`/`loaddata` pasan por el ORM: tarda muchisimo mas, se atraganca con
las referencias circulares y no reproduce secuencias, indices ni triggers. Un
volcado en formato custom si, y ademas pesa una fraccion.

El origen sale de .env.prod y el destino de la configuracion cargada, que es
.env.dev salvo que alguien cambie DJANGO_ENV. Como el primer paso de la
restauracion es destruir el esquema public, antes de tocar nada se comprueba
que el destino es esta maquina y que no coincide con el origen: un
DJANGO_ENV=prod de mas, y lo que se borraria es produccion.

La base de DigitalOcean solo admite las IP que figuran en Trusted Sources, asi
que desde una maquina de casa el volcado no conecta. Para eso estan los dos
modos partidos: se vuelca en el servidor y se restaura aqui desde el archivo.

    manage.py clonar_db_produccion                      # muestra el plan
    manage.py clonar_db_produccion --aplicar            # vuelca y restaura
    manage.py clonar_db_produccion --aplicar --solo-descargar   # en el servidor
    manage.py clonar_db_produccion --aplicar --desde data/backups/x.dump

El archivo queda en data/backups/, que no se versiona, y contiene los datos
reales de los clientes: correos, telefonos y hashes de contrasena. No sale de
la maquina.
"""

import os
import re
import shutil
import subprocess
from datetime import datetime
from glob import glob
from pathlib import Path

import environ

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection


# El destino tiene que estar en esta maquina. No es una formalidad: la
# restauracion empieza borrando el esquema public, y apuntada a un host remoto
# por descuido el borrado seria el de produccion.
LOCALES = {'127.0.0.1', '::1', 'localhost'}

# En Windows los binarios de postgres no se ponen en el PATH al instalar.
CARPETAS_CANDIDATAS = (
    'C:/Program Files/PostgreSQL/*/bin',
    '/usr/lib/postgresql/*/bin',
    '/usr/pgsql-*/bin',
)

# El nombre de la base entra en un CREATE DATABASE y en un WHERE, donde no se
# puede parametrizar. Viniendo del .env el riesgo es remoto, pero comprobarlo
# cuesta una linea.
NOMBRE_VALIDO = re.compile(r'^[A-Za-z0-9_]+$')

# Primero el lock_timeout: sin el, un runserver olvidado con la base abierta
# deja el DROP esperando para siempre en vez de fallar y decirlo.
SQL_VACIAR = """
SET lock_timeout = '10s';
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;
"""

SQL_RESUMEN = """
SELECT relname, n_live_tup
  FROM pg_stat_user_tables
 ORDER BY n_live_tup DESC, relname
 LIMIT 12
"""

# Los fallos de pg_dump y pg_restore se explican solos para quien conoce
# postgres; estos son los que tienen una causa concreta en este proyecto.
PISTAS = (
    (('timeout expired', 'could not connect', 'connection timed out',
      'no route to host', 'operation timed out'),
     'El servidor no contesta. La base de DigitalOcean solo acepta las IP que\n'
     'figuran en Trusted Sources: anade la de esta maquina en el panel, o haz el\n'
     'volcado en el servidor con --solo-descargar y traete el archivo.'),
    (('password authentication failed', 'authentication failed'),
     'Usuario o contrasena rechazados: revisa DB_USER y DB_PASSWORD en .env.prod.'),
    (('server version', 'version mismatch'),
     'El cliente es mas antiguo que el servidor y pg_dump se niega a volcar.\n'
     'Instala el cliente de la version del servidor y apunta ahi con --pg-bin.'),
    (('lock timeout', 'canceling statement due to lock'),
     'Otra sesion tiene tomadas las tablas. Cierra runserver, el shell de Django\n'
     'y las ventanas de pgAdmin o DBeaver, y repite.'),
    (('does not exist',),
     'Falta la base o el rol. Revisa DB_NAME y DB_USER del entorno que toca.'),
)


class Conexion:
    """Los datos de una base. La etiqueta nunca lleva la contrasena."""

    def __init__(self, nombre, usuario, contrasena, host, puerto, sslmode):
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.host = host
        self.puerto = str(puerto)
        self.sslmode = sslmode

    @property
    def etiqueta(self):
        return '{}@{}:{}/{}'.format(self.usuario, self.host, self.puerto, self.nombre)

    @property
    def es_local(self):
        return self.host in LOCALES

    @property
    def senas(self):
        return (self.host, self.puerto, self.nombre)

    def entorno(self):
        """El entorno con el que se lanzan los binarios de postgres.

        La contrasena viaja aqui y no en la linea de ordenes porque los
        argumentos de un proceso los lee cualquiera con `ps` o con el
        administrador de tareas. PGCONNECT_TIMEOUT esta puesto para que un
        cortafuegos cerrado se note en quince segundos en vez de dejar el
        comando colgado los dos minutos que tarda el sistema en rendirse.
        """
        return dict(
            os.environ,
            PGPASSWORD=self.contrasena,
            PGSSLMODE=self.sslmode,
            PGCONNECT_TIMEOUT='15',
            PGCLIENTENCODING='UTF8',
        )

    def argumentos(self, base=None):
        # --no-password en todas: si la contrasena no sirve, se quiere el error
        # y no un prompt que deje el comando esperando a un teclado que no hay.
        return ['--host', self.host, '--port', self.puerto,
                '--username', self.usuario, '--no-password',
                '--dbname', base or self.nombre]


def _version_de(carpeta):
    """El numero de version que lleva la carpeta de instalacion."""
    encontrado = re.search(r'(\d+(?:\.\d+)?)', Path(carpeta).parent.name)
    return float(encontrado.group(1)) if encontrado else 0.0


def _binarios(carpeta_pedida):
    """Localiza pg_dump, pg_restore y psql.

    Con --pg-bin se busca solo ahi, para que una carpeta mal escrita se note en
    vez de resolverse por detras con otra version. Sin el, primero el PATH y
    despues las instalaciones del sistema, de la version mas alta a la mas
    baja: pg_dump se niega a volcar de un servidor mas nuevo que el, y el de
    produccion suele ir por delante del local.
    """
    if carpeta_pedida:
        carpetas = [carpeta_pedida]
        mirar_el_path = False
    else:
        carpetas = []
        for patron in CARPETAS_CANDIDATAS:
            carpetas.extend(glob(patron))
        carpetas.sort(key=_version_de, reverse=True)
        mirar_el_path = True

    encontrados = {}
    for nombre in ('pg_dump', 'pg_restore', 'psql'):
        ruta = shutil.which(nombre) if mirar_el_path else None
        for carpeta in carpetas:
            if ruta:
                break
            ruta = shutil.which(nombre, path=str(carpeta))
        if not ruta:
            raise CommandError(
                'No encuentro {}. Es parte del cliente de PostgreSQL.\n'
                'Si esta instalado pero fuera del PATH, pasa su carpeta:\n'
                '    --pg-bin "C:/Program Files/PostgreSQL/17/bin"'.format(nombre))
        encontrados[nombre] = ruta
    return encontrados


def _explicar(herramienta, salida):
    mensaje = '{} fallo.\n\n{}'.format(herramienta, (salida or '').strip())
    minusculas = (salida or '').lower()
    for senales, pista in PISTAS:
        if any(senal in minusculas for senal in senales):
            return '{}\n\n{}'.format(mensaje, pista)
    return mensaje


def _correr(orden, entorno, herramienta):
    proceso = subprocess.run(orden, env=entorno, capture_output=True,
                             text=True, encoding='utf-8', errors='replace')
    if proceso.returncode != 0:
        raise CommandError(_explicar(herramienta, proceso.stderr or proceso.stdout))
    return proceso.stdout or ''


def _conexion_de_archivo(ruta):
    """Lee un .env sin pisar las variables del proceso.

    read_env escribe en Env.ENVIRON, que por defecto es os.environ. Leer
    .env.prod ahi dejaria las credenciales de produccion en el entorno de un
    proceso que esta corriendo con las de desarrollo, asi que la subclase se
    queda con un diccionario propio. Se declara aqui dentro para que cada
    lectura empiece vacia.
    """
    if not ruta.is_file():
        raise CommandError('No existe {}. Es de donde salen las credenciales de '
                           'produccion.'.format(ruta))

    class Aislado(environ.Env):
        ENVIRON = {}

    Aislado.read_env(str(ruta), overwrite=True)
    entorno = Aislado()
    return Conexion(
        nombre=entorno.str('DB_NAME'),
        usuario=entorno.str('DB_USER'),
        contrasena=entorno.str('DB_PASSWORD'),
        host=entorno.str('DB_HOST'),
        puerto=entorno.int('DB_PORT'),
        sslmode=entorno.str('DB_SSLMODE'),
    )


def _conexion_cargada():
    """La base a la que apunta la configuracion con la que arranco Django."""
    ajustes = settings.DATABASES['default']
    return Conexion(
        nombre=ajustes['NAME'],
        usuario=ajustes['USER'],
        contrasena=ajustes['PASSWORD'],
        host=ajustes['HOST'],
        puerto=ajustes['PORT'],
        sslmode=ajustes.get('OPTIONS', {}).get('sslmode', 'prefer'),
    )


class Command(BaseCommand):
    help = 'Vuelca la base de produccion y la restaura sobre la base local.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--aplicar', action='store_true',
            help='Ejecuta. Sin esto solo se muestra el plan y no se escribe nada.')
        parser.add_argument(
            '--solo-descargar', action='store_true', dest='solo_descargar',
            help='Vuelca a un archivo y no restaura. Para lanzarlo en el servidor.')
        parser.add_argument(
            '--desde', metavar='ARCHIVO',
            help='Restaura este volcado en vez de descargar uno nuevo.')
        parser.add_argument(
            '--salida', metavar='ARCHIVO',
            help='Donde dejar el volcado. Por defecto data/backups/produccion-<fecha>.dump')
        parser.add_argument(
            '--env-prod', metavar='ARCHIVO', dest='env_prod',
            help='El .env del que leer el origen. Por defecto .env.prod del proyecto.')
        parser.add_argument(
            '--pg-bin', metavar='CARPETA', dest='pg_bin',
            help='La carpeta con pg_dump, pg_restore y psql, si no estan en el PATH.')

    def handle(self, *args, **opciones):
        desde = Path(opciones['desde']).expanduser() if opciones['desde'] else None
        solo_descargar = opciones['solo_descargar']

        if desde and solo_descargar:
            raise CommandError('--desde y --solo-descargar se excluyen: uno restaura '
                               'un archivo y el otro lo genera.')

        origen = None if desde else self._origen(opciones['env_prod'])
        destino = None if solo_descargar else _conexion_cargada()
        archivo = self._archivo(desde, opciones['salida'])

        if destino:
            self._comprobar_destino(destino, origen)

        self._mostrar_plan(origen, destino, archivo, desde is not None)
        if not opciones['aplicar']:
            self.stdout.write(self.style.WARNING(
                'Nada escrito. Repite con --aplicar cuando el plan sea el que quieres.'))
            return

        binarios = _binarios(opciones['pg_bin'])

        if origen:
            self._volcar(origen, archivo, binarios)
        if destino:
            self._restaurar(destino, archivo, binarios)
            self._comprobar_resultado(destino, binarios)
            self._avisos(archivo)
        else:
            self.stdout.write('')
            self.stdout.write('Llevate el archivo a la maquina de desarrollo y restaura con:')
            self.stdout.write('    manage.py clonar_db_produccion --aplicar --desde {}'
                              .format(archivo.name))

    # ------------------------------------------------------------- preparacion

    def _origen(self, env_prod):
        ruta = Path(env_prod).expanduser() if env_prod else Path(settings.BASE_DIR) / '.env.prod'
        return _conexion_de_archivo(ruta)

    def _archivo(self, desde, salida):
        if desde:
            if not desde.is_file():
                raise CommandError('No existe el volcado {}'.format(desde))
            return desde
        if salida:
            return Path(salida).expanduser()
        carpeta = Path(settings.PATH_BASE) / 'backups'
        sello = datetime.now().strftime('%Y%m%d-%H%M')
        return carpeta / 'produccion-{}.dump'.format(sello)

    def _comprobar_destino(self, destino, origen):
        """Las dos preguntas que hay que contestar antes de borrar un esquema."""
        if origen and origen.senas == destino.senas:
            raise CommandError(
                'El origen y el destino son la misma base ({}).\n'
                'Esto restauraria produccion sobre produccion. Lo normal es que '
                'DJANGO_ENV este en prod; ejecuta con DJANGO_ENV=dev.'.format(destino.etiqueta))
        if not destino.es_local:
            raise CommandError(
                'El destino {} no esta en esta maquina.\n'
                'La restauracion borra el esquema public antes de escribir, asi que '
                'solo se permite contra 127.0.0.1 o localhost. Revisa DB_HOST del '
                'entorno cargado y DJANGO_ENV.'.format(destino.etiqueta))
        if not NOMBRE_VALIDO.match(destino.nombre):
            raise CommandError('El nombre de la base local ({!r}) tiene caracteres que '
                               'habria que citar; renombrala.'.format(destino.nombre))

    def _mostrar_plan(self, origen, destino, archivo, reutiliza):
        self.stdout.write('')
        self.stdout.write(self.style.MIGRATE_HEADING('Plan'))
        if origen:
            self.stdout.write('  origen   {}'.format(origen.etiqueta))
        if reutiliza:
            megas = archivo.stat().st_size / 1048576.0
            self.stdout.write('  archivo  {}  ({:.1f} MB, ya descargado)'.format(archivo, megas))
        else:
            self.stdout.write('  archivo  {}'.format(archivo))
        if destino:
            self.stdout.write('  destino  {}'.format(destino.etiqueta))
            self.stdout.write(self.style.WARNING(
                '           se borra su esquema public con todo lo que tenga'))
        else:
            self.stdout.write('  destino  ninguno, solo se descarga')
        self.stdout.write('')

    # ------------------------------------------------------------------ trabajo

    def _volcar(self, origen, archivo, binarios):
        archivo.parent.mkdir(parents=True, exist_ok=True)
        self.stdout.write('Volcando {} ...'.format(origen.etiqueta))
        orden = ([binarios['pg_dump'], '--format=custom', '--compress=6',
                  '--no-owner', '--no-privileges']
                 + origen.argumentos() + ['--file', str(archivo)])
        try:
            _correr(orden, origen.entorno(), 'pg_dump')
        except CommandError:
            # Un volcado a medias es peor que ninguno: parece valido y pg_restore
            # lo rechaza mucho despues, cuando ya se borro el esquema local.
            if archivo.exists():
                archivo.unlink()
            raise
        megas = archivo.stat().st_size / 1048576.0
        self.stdout.write(self.style.SUCCESS('  {}  ({:.1f} MB)'.format(archivo, megas)))

    def _restaurar(self, destino, archivo, binarios):
        # Django mantiene su propia conexion abierta a esta base y el DROP SCHEMA
        # se quedaria esperando a que la suelte.
        connection.close()
        entorno = destino.entorno()

        self._crear_si_falta(destino, binarios, entorno)

        self.stdout.write('Vaciando el esquema public de {} ...'.format(destino.etiqueta))
        _correr([binarios['psql'], '--quiet', '--set', 'ON_ERROR_STOP=on']
                + destino.argumentos() + ['--command', SQL_VACIAR], entorno, 'psql')

        self.stdout.write('Restaurando {} ...'.format(archivo.name))
        # --single-transaction: o entra el volcado entero o no entra nada. Una
        # base a medias corre y falla en sitios raros dias despues.
        _correr([binarios['pg_restore'], '--no-owner', '--no-privileges',
                 '--single-transaction'] + destino.argumentos() + [str(archivo)],
                entorno, 'pg_restore')

    def _crear_si_falta(self, destino, binarios, entorno):
        consulta = "SELECT 1 FROM pg_database WHERE datname = '{}'".format(destino.nombre)
        hay = _correr([binarios['psql'], '--tuples-only', '--no-align']
                      + destino.argumentos(base='postgres') + ['--command', consulta],
                      entorno, 'psql')
        if hay.strip() == '1':
            return
        self.stdout.write('La base {} no existe todavia; la creo.'.format(destino.nombre))
        _correr([binarios['psql']] + destino.argumentos(base='postgres')
                + ['--command', 'CREATE DATABASE "{}"'.format(destino.nombre)],
                entorno, 'psql')

    # ------------------------------------------------------------ comprobacion

    def _comprobar_resultado(self, destino, binarios):
        """Contar filas, porque terminar sin error no es tener datos.

        ANALYZE no esta solo para poder contarlas: un clon recien restaurado no
        tiene estadisticas, y hasta que alguien las calcula el planificador
        elige planes malos y las paginas de busqueda van lentas sin motivo.
        """
        entorno = destino.entorno()
        self.stdout.write('Calculando estadisticas ...')
        _correr([binarios['psql'], '--quiet'] + destino.argumentos()
                + ['--command', 'ANALYZE'], entorno, 'psql')

        salida = _correr([binarios['psql'], '--tuples-only', '--no-align',
                          '--field-separator', '\t'] + destino.argumentos()
                         + ['--command', SQL_RESUMEN], entorno, 'psql')
        filas = [linea.split('\t') for linea in salida.splitlines() if '\t' in linea]
        if not filas:
            raise CommandError(
                'La restauracion termino sin error pero la base quedo sin tablas. '
                'El volcado esta vacio o no es de esta base.')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Restaurado. Las tablas con mas filas:'))
        for tabla, cuantas in filas:
            self.stdout.write('  {:>9}  {}'.format(cuantas, tabla))

    def _avisos(self, archivo):
        self.stdout.write('')
        self.stdout.write(self.style.MIGRATE_HEADING('Despues de esto'))
        self.stdout.write(
            '  - manage.py migrate, si el codigo local tiene migraciones que\n'
            '    produccion todavia no ha aplicado.')
        self.stdout.write(
            '  - Los usuarios son los de produccion y sus contrasenas no se\n'
            '    conocen: manage.py createsuperuser para entrar al admin.')
        self.stdout.write(
            '  - Las fichas apuntan a las imagenes del bucket de produccion; con\n'
            '    USE_SPACES=False en .env.dev se veran rotas.')
        self.stdout.write(
            '  - {}\n'
            '    tiene datos reales de clientes. No se sube a ningun sitio y se\n'
            '    borra cuando deje de hacer falta.'.format(archivo))
