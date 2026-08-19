"""Sincroniza los estaticos con Spaces sin preguntar archivo por archivo.

collectstatic tarda unos minutos aunque no haya nada que subir, y el motivo
no son los bytes sino la latencia. Para cada uno de los 2142 archivos hace
dos peticiones a Spaces en serie -- una para saber si existe y otra para su
fecha -- y espera la respuesta antes de pasar al siguiente. Son 4284 viajes
de ida y vuelta a San Francisco.

Aqui se hacen dos cambios:

  - El inventario del bucket se pide de una sola vez. list_objects_v2
    devuelve 1000 objetos por peticion, con su tamano y su ETag, asi que los
    3197 caben en 4 llamadas en vez de 4284. El ETag de un objeto subido de
    una pieza es su MD5, de modo que comparar el contenido no cuesta ni una
    peticion mas: el MD5 del archivo local se calcula en disco.

  - Lo que haya que subir se sube en paralelo. Son transferencias
    independientes y el limite es la latencia, no el ancho de banda.

Con todo al dia baja de varios minutos a unos segundos, y una subida
completa se reparte entre los hilos.

Uso:
    python manage.py sync_static
    python manage.py sync_static --dry-run     # dice que subiria, no sube
    python manage.py sync_static --workers 32
"""

import hashlib
import mimetypes
import os
import threading
from concurrent.futures import ThreadPoolExecutor

import boto3

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.management.base import BaseCommand, CommandError

# Un ETag con guion viene de una subida multiparte y entonces NO es el MD5
# del archivo, sino un hash de hashes. Esos se comparan por tamano.
MULTIPARTE = '-'

# Al servir texto conviene declarar la codificacion: bundle.js lleva acentos
# en las cadenas del switch de checkForModalParameter y bundle.css flechas de
# menu en content:. Sin charset el navegador tiene que adivinarlo.
TEXTO = {'.js', '.css', '.json', '.svg', '.txt', '.map', '.html', '.xml'}

# Los mismos que descarta collectstatic por defecto. Importa respetarlos: sin
# ellos se suben los .DS_Store que deja macOS por cada carpeta, que el bucket
# no tiene justamente porque collectstatic nunca los subio.
IGNORAR = ['CVS', '.*', '*~']

_local = threading.local()


class Command(BaseCommand):
    help = 'Sube a Spaces solo los estaticos que cambiaron, en paralelo.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run', action='store_true',
            help='Informa de lo que subiria, sin subir nada.')
        parser.add_argument(
            '--workers', type=int, default=16,
            help='Subidas simultaneas (por defecto 16).')

    def handle(self, *args, **options):
        self.opciones = self._config()

        self.stdout.write('Pidiendo el inventario del bucket...')
        remoto = self._inventario()
        self.stdout.write('  %d objetos bajo %s/' % (len(remoto), self.prefijo))

        self.stdout.write('Comparando con el repositorio...')
        pendientes, iguales = self._comparar(remoto)
        self.stdout.write('  %d al dia, %d por subir' % (iguales, len(pendientes)))

        if not pendientes:
            self.stdout.write(self.style.SUCCESS('Spaces ya esta al dia.'))
            return

        if options['dry_run']:
            for ruta, _, motivo in pendientes[:50]:
                self.stdout.write('  + %-60s %s' % (ruta, motivo))
            if len(pendientes) > 50:
                self.stdout.write('  ... y %d mas' % (len(pendientes) - 50))
            self.stdout.write(self.style.WARNING(
                'Simulacion: no se ha subido nada.'))
            return

        self.stdout.write('Subiendo con %d hilos...' % options['workers'])
        with ThreadPoolExecutor(max_workers=options['workers']) as pool:
            for hechos, _ in enumerate(pool.map(self._subir, pendientes), start=1):
                if hechos % 100 == 0 or hechos == len(pendientes):
                    self.stdout.write('  %d/%d' % (hechos, len(pendientes)))

        self.stdout.write(self.style.SUCCESS(
            '%d archivos subidos a Spaces.' % len(pendientes)))

    # -- configuracion ----------------------------------------------------

    def _config(self):
        """Credenciales y destino, los mismos que usa el almacenamiento."""
        try:
            opciones = {
                'access_key': settings.AWS_S3_ACCESS_KEY_ID,
                'secret_key': settings.AWS_S3_SECRET_ACCESS_KEY,
                'bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'endpoint': settings.AWS_S3_ENDPOINT_URL,
            }
        except AttributeError as error:
            raise CommandError(
                'Falta la configuracion de Spaces en local_settings: %s' % error)

        # El prefijo sale de STORAGES si esta definido (produccion); en
        # desarrollo ese bloque no existe y el valor es el mismo de siempre.
        almacen = getattr(settings, 'STORAGES', {}).get('staticfiles', {})
        self.prefijo = almacen.get('OPTIONS', {}).get('location', 'static')
        return opciones

    def _cliente(self):
        """Un cliente por hilo: botocore no garantiza poder compartirlos."""
        if not hasattr(_local, 'cliente'):
            _local.cliente = boto3.client(
                's3',
                endpoint_url=self.opciones['endpoint'],
                aws_access_key_id=self.opciones['access_key'],
                aws_secret_access_key=self.opciones['secret_key'])
        return _local.cliente

    # -- comparacion ------------------------------------------------------

    def _inventario(self):
        """Todo el bucket en 4 peticiones en vez de una por archivo."""
        cliente = self._cliente()
        remoto = {}
        token = None
        while True:
            extra = {'ContinuationToken': token} if token else {}
            respuesta = cliente.list_objects_v2(
                Bucket=self.opciones['bucket'],
                Prefix=self.prefijo + '/', MaxKeys=1000, **extra)
            for objeto in respuesta.get('Contents', []):
                clave = objeto['Key'][len(self.prefijo) + 1:]
                remoto[clave] = (objeto['ETag'].strip('"'), objeto['Size'])
            if not respuesta.get('IsTruncated'):
                return remoto
            token = respuesta['NextContinuationToken']

    def _locales(self):
        """Los mismos archivos que recogeria collectstatic, sin duplicados."""
        vistos = {}
        for finder in finders.get_finders():
            for ruta, almacen in finder.list(IGNORAR):
                vistos.setdefault(ruta.replace(os.sep, '/'), almacen.path(ruta))
        return vistos

    def _comparar(self, remoto):
        pendientes, iguales = [], 0
        for ruta, absoluta in sorted(self._locales().items()):
            etag, tamano = remoto.get(ruta, (None, None))
            local = os.path.getsize(absoluta)

            if etag is None:
                pendientes.append((ruta, absoluta, 'no esta en el bucket'))
            elif MULTIPARTE in etag:
                # Sin MD5 fiable solo queda el tamano. Se subio en varias
                # partes, asi que es un archivo grande y conviene no volver a
                # moverlo sin motivo.
                if local != tamano:
                    pendientes.append((ruta, absoluta, 'tamano distinto'))
                else:
                    iguales += 1
            elif local != tamano or self._md5(absoluta) != etag:
                pendientes.append((ruta, absoluta, 'contenido distinto'))
            else:
                iguales += 1
        return pendientes, iguales

    def _md5(self, absoluta):
        resumen = hashlib.md5()
        with open(absoluta, 'rb') as fichero:
            for trozo in iter(lambda: fichero.read(1024 * 1024), b''):
                resumen.update(trozo)
        return resumen.hexdigest()

    # -- subida -----------------------------------------------------------

    def _subir(self, pendiente):
        ruta, absoluta, _ = pendiente
        with open(absoluta, 'rb') as fichero:
            cuerpo = fichero.read()
        self._cliente().put_object(
            Bucket=self.opciones['bucket'],
            Key='%s/%s' % (self.prefijo, ruta),
            Body=cuerpo,
            ContentType=self._tipo(ruta),
            ACL='public-read')
        return ruta

    def _tipo(self, ruta):
        tipo = mimetypes.guess_type(ruta)[0] or 'application/octet-stream'
        if os.path.splitext(ruta)[1].lower() in TEXTO and 'charset' not in tipo:
            tipo += '; charset=utf-8'
        return tipo
