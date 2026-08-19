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

    def handle(self, *args, **options):
        solo_comprobar = options['check']
        rutas = CRITICOS + options['extra']

        if not solo_comprobar:
            if settings.DEBUG:
                raise CommandError(
                    'Con DEBUG=True el almacenamiento de estaticos es el disco '
                    'local, no Spaces: collectstatic no subiria nada al bucket. '
                    'Ejecutelo en el servidor, o use --check para solo verificar.')

            self.stdout.write(self.style.MIGRATE_HEADING('1/3 Generando los bundles'))
            call_command('build_bundles')

            self.stdout.write(self.style.MIGRATE_HEADING('2/3 Subiendo a Spaces'))
            call_command('collectstatic', interactive=False, verbosity=1)

        self.stdout.write(self.style.MIGRATE_HEADING(
            '3/3 Verificando lo que se sirve' if not solo_comprobar
            else 'Verificando lo que se sirve'))

        fallos = []
        for ruta in rutas:
            error = self._verificar(ruta)
            if error:
                fallos.append('%s: %s' % (ruta, error))

        if fallos:
            raise CommandError(
                'Los estaticos NO se estan sirviendo correctamente:\n  - %s\n'
                'Si acaba de subirlos, el edge del CDN puede tardar en refrescar; '
                'vuelva a ejecutar con --check antes de dar nada por roto.'
                % '\n  - '.join(fallos))

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
            return ('%s sirve una version distinta (local %s, servido %s)'
                    % (url, esperado[:12], servido[:12]))

        self.stdout.write('  = %-22s %d KB, %s' % (
            ruta, len(respuesta.content) / 1024, esperado[:12]))
        return None

    def _url_publica(self, ruta):
        """URL por la que el navegador pide el estatico.

        Con DEBUG=False el almacenamiento ya devuelve la URL absoluta del edge.
        Con DEBUG=True devuelve /static/..., que no sirve para comprobar nada,
        asi que se compone la de produccion: verificar desde la maquina de
        desarrollo si el bucket esta al dia es justo para lo que hace falta.
        """
        url = staticfiles_storage.url(ruta)
        if url.startswith('http'):
            return url

        region = urlsplit(settings.AWS_S3_ENDPOINT_URL).netloc.split('.')[0]
        return 'https://{}.{}.cdn.digitaloceanspaces.com/static/{}'.format(
            settings.AWS_STORAGE_BUCKET_NAME, region, ruta)

    def _en_disco(self, ruta):
        """Respaldo para cuando los finders no miran BASE_DIR/static (DEBUG=False)."""
        candidato = os.path.join(str(settings.BASE_DIR), 'static',
                                 ruta.replace('/', os.sep))
        return candidato if os.path.exists(candidato) else None

    def _sha1(self, datos):
        return hashlib.sha1(datos).hexdigest()
