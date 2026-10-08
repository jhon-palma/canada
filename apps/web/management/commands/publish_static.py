"""Publica los estaticos en Spaces y comprueba que de verdad llegaron.

Los bundles del header se versionan en el repositorio, asi que un `git pull`
en el servidor los deja en disco, pero el navegador no los lee de ahi: los
pide al edge del CDN de Spaces. Si nadie sube el archivo al bucket, la
peticion responde 404 y la pagina se queda sin estilos y sin las funciones
del header (checkForModalParameter, changeParameterInURL...). Eso fue
exactamente lo que paso al unificar los bundles.

Este comando es el paso de despliegue que faltaba. Hace las tres cosas en
orden y aborta en cuanto una falla:

  1. build_bundles, para que el bundle refleje los originales del repositorio.
  2. collectstatic, que sube a Spaces con ACL public-read.
  3. Descarga por HTTP las URLs que Django emite en las plantillas y compara
     el sha1 con el archivo local.

El tercer paso es el que importa: los dos primeros pueden terminar sin error
y dejar el sitio roto igualmente (un prefijo mal puesto, un finder que no
mira donde crees, el edge sirviendo otra cosa). Comprobar el byte servido es
la unica prueba de que la pagina funciona.

Uso, en el servidor y con DEBUG=False:

    python manage.py publish_static
    python manage.py publish_static --check    # no sube, solo verifica
"""

import hashlib
import io
import os
from urllib.parse import urlsplit

import requests

from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from apps.estaticos import versionar

# Lo que el header carga en todas las paginas: si alguno de estos falta, el
# sitio se ve roto entero, no solo una seccion.
CRITICOS = [
    'web/css/bundle.css',
    'web/js/bundle.js',
]


class Command(BaseCommand):
    help = 'Genera los bundles, sube los estaticos a Spaces y verifica que se sirven.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--check', action='store_true',
            help='No genera ni sube nada: solo verifica lo que se esta sirviendo.')
        parser.add_argument(
            '--verificar', dest='extra', action='append', default=[],
            help='Ruta estatica adicional a verificar. Se puede repetir.')
        parser.add_argument(
            '--workers', type=int, default=16,
            help='Subidas simultaneas en el paso 2 (por defecto 16).')
        parser.add_argument(
            '--dry-run', action='store_true',
            help='Ensayo: dice que subiria el paso 2, pero no sube nada.')

    def handle(self, *args, **options):
        solo_comprobar = options['check']
        rutas = CRITICOS + options['extra']

        if not solo_comprobar:
            self.stdout.write(self.style.MIGRATE_HEADING('1/3 Generando los bundles'))
            call_command('build_bundles')

            self.stdout.write(self.style.MIGRATE_HEADING('2/3 Subiendo a Spaces'))
            call_command('sync_static', workers=options['workers'],
                         dry_run=options['dry_run'])

        self.stdout.write(self.style.MIGRATE_HEADING(
            '3/3 Verificando lo que se sirve' if not solo_comprobar
            else 'Verificando lo que se sirve'))

        self.cache_sucia = []
        fallos = []
        for ruta in rutas:
            error = self._verificar(ruta)
            if error:
                fallos.append('%s: %s' % (ruta, error))

        if fallos:
            partes = ['Los estaticos NO se estan sirviendo correctamente:',
                      '  - ' + '\n  - '.join(fallos)]
            if self.cache_sucia:
                partes.append(
                    'El bucket esta bien: lo que sirve copias viejas es la cache del\n'
                    'CDN, y no caduca sola hasta siete dias. Purguela y repita con\n'
                    '--check. Se purga en el panel de Spaces, o desde Cloudflare si\n'
                    'el dominio esta detras suyo. Rutas:\n'
                    + '\n'.join('  static/%s' % r for r in self.cache_sucia))
            raise CommandError('\n'.join(partes))

        self.stdout.write(self.style.SUCCESS(
            'Los %d estaticos verificados se sirven y coinciden con el repositorio.'
            % len(rutas)))

    def _verificar(self, ruta):
        """Devuelve None si la URL publica sirve el mismo byte que el archivo local."""
        local = finders.find(ruta) or self._en_disco(ruta)
        if not local:
            return 'no existe en el repositorio (busque un error de ruta)'

        esperado = self._sha1(io.open(local, 'rb').read())
        url = self._url_publica(ruta)

        try:
            respuesta = requests.get(url, timeout=30)
        except requests.RequestException as error:
            return 'no se pudo descargar %s (%s)' % (url, error)

        if respuesta.status_code != 200:
            return 'HTTP %d en %s' % (respuesta.status_code, url)

        servido = self._sha1(respuesta.content)
        if servido != esperado:
            return self._diagnosticar(ruta, esperado, servido)

        self.stdout.write('  = %-22s %d KB, %s' % (
            ruta, len(respuesta.content) / 1024, esperado[:12]))
        return None

    def _diagnosticar(self, ruta, esperado, servido):
        """Separa "no se subio" de "el edge sirve una copia vieja".

        Son dos averias distintas con dos arreglos distintos, y antes este
        paso daba por hecho la primera: el mensaje mandaba a comprobar que la
        subida hubiese llegado al bucket. El 7 de octubre de 2026 el bucket
        estaba perfecto y lo viejo lo servia el edge, asi que media hora se
        fue en buscar un fallo de subida que no existia.

        Distinguirlas cuesta una peticion mas: el mismo archivo pedido al
        bucket, sin pasar por el CDN. Si ahi coincide con el repositorio, la
        subida fue bien y lo unico que falta es purgar.
        """
        origen = self._url_origen(ruta)
        try:
            respuesta = requests.get(origen, timeout=30)
        except requests.RequestException as error:
            return ('el edge sirve otra version (local %s, edge %s) y no se pudo '
                    'preguntar al bucket para saber por que (%s)'
                    % (esperado[:12], servido[:12], error))

        if respuesta.status_code != 200:
            return ('el edge sirve otra version (local %s, edge %s) y el bucket '
                    'responde HTTP %d en %s'
                    % (esperado[:12], servido[:12], respuesta.status_code, origen))

        en_bucket = self._sha1(respuesta.content)
        if en_bucket == esperado:
            self.cache_sucia.append(ruta)
            return ('el bucket lo tiene correcto y el edge sirve una copia vieja '
                    '(local %s, edge %s)' % (esperado[:12], servido[:12]))

        return ('el bucket no lo tiene correcto (local %s, bucket %s): la subida '
                'del paso 2 no llego' % (esperado[:12], en_bucket[:12]))

    def _url_origen(self, ruta):
        """La URL del archivo en el bucket, sin pasar por el edge.

        Es la del CDN sin el '.cdn.', que es lo unico que separa el dominio
        del edge del de Spaces. Sin marca de version: al bucket se le pide el
        objeto, no una variante.
        """
        region = urlsplit(settings.AWS_S3_ENDPOINT_URL).netloc.split('.')[0]
        return 'https://{}.{}.digitaloceanspaces.com/static/{}'.format(
            settings.AWS_STORAGE_BUCKET_NAME, region, ruta)

    def _url_publica(self, ruta):
        """URL por la que el navegador pide el estatico.

        Con DEBUG=False el almacenamiento ya devuelve la URL absoluta del edge.
        Con DEBUG=True devuelve /static/..., que no sirve para comprobar nada,
        asi que se compone la de produccion: verificar desde la maquina de
        desarrollo si el bucket esta al dia es justo para lo que hace falta.

        Lleva la misma marca ?v= que emite el tag static_v en las plantillas,
        para comprobar exactamente la URL que pide el navegador y no otra
        parecida.

        Lo que la marca NO hace es saltarse la cache del edge, aunque sea para
        lo que suele ponerse. El CDN de Spaces ignora la query string al
        calcular la clave, asi que ?v=nuevo y ?v=viejo son la misma entrada.
        Medido el 7 de octubre de 2026: el edge devolvio un objeto con
        last-modified del 26 de agosto para un ?v= recien generado. De ahi que
        una version nueva pueda quedarse semanas sin llegar a nadie, y que
        este paso tenga que preguntarle al bucket para saber a quien culpar.
        """
        url = staticfiles_storage.url(ruta)
        if not url.startswith('http'):
            region = urlsplit(settings.AWS_S3_ENDPOINT_URL).netloc.split('.')[0]
            url = 'https://{}.{}.cdn.digitaloceanspaces.com/static/{}'.format(
                settings.AWS_STORAGE_BUCKET_NAME, region, ruta)

        return versionar(url, ruta)

    def _en_disco(self, ruta):
        """Respaldo para cuando los finders no miran BASE_DIR/static (DEBUG=False)."""
        candidato = os.path.join(str(settings.BASE_DIR), 'static',
                                 ruta.replace('/', os.sep))
        return candidato if os.path.exists(candidato) else None

    def _sha1(self, datos):
        return hashlib.sha1(datos).hexdigest()
