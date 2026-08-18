"""Une los CSS y JS de la portada en dos archivos.

El header cargaba 9 CSS y 2 JS propios. Ya vienen comprimidos desde el edge
del CDN (56 KiB en total), pero tardaban 9760 ms: el coste ya no son los
bytes sino las once conexiones bajo una red movil lenta. Unificarlos deja
dos peticiones.

Decisiones:

- No se minifica. Sobre el gzip que ya aplica el edge, minificar solo
  aportaba un 17% (36 KB -> 30 KB), y un minificador propio es una fuente
  de fallos sutiles en CSS (cadenas, data: URIs) y en JS (punto y coma
  automatico). Concatenar es verificable byte a byte; minificar no.

- El CSS unificado se escribe en la MISMA carpeta que los originales
  (web/css/). Los 9 archivos comparten carpeta y contienen 62 rutas
  relativas tipo url(../images/bed.svg): generandolo ahi siguen resolviendo
  y no hay que reescribir nada.

- Se respeta el orden del header, del que depende la cascada.

- @charset solo es valido como primeros bytes del archivo, asi que se emite
  una vez al principio del bundle y se retira de los originales.

Hay que volver a ejecutarlo cada vez que se edite alguno de los archivos de
origen, o el sitio servira la version anterior.
"""

import io
import os
import re

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

# Mismo orden que en templates/web/header_web.html: la cascada depende de el.
CSS_SOURCES = [
    'web/css/stylesheet.css',
    'web/css/styles-policy.css',
    'web/css/responsive.css',
    'web/css/responsiveslides.css',
    'web/css/styles.css',
    'web/css/master.css',
    'web/css/jenner.css',
    'web/css/jquery.mmenu.positioning.css',
    'web/css/jquery.mmenu.all.css',
]
CSS_BUNDLE = 'web/css/bundle.css'

JS_SOURCES = [
    'web/js/main.js',
    'app/js/functions/master.js',
]
JS_BUNDLE = 'web/js/bundle.js'

CHARSET_RE = re.compile(r'^\s*@charset\s+["\'][^"\']*["\']\s*;', re.I)


class Command(BaseCommand):
    help = 'Genera web/css/bundle.css y web/js/bundle.js a partir de los archivos del header.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--check', action='store_true',
            help='No escribe: informa de si los bundles estan al dia.')

    def handle(self, *args, **options):
        base = self._static_dir()
        solo_comprobar = options['check']
        desactualizados = []

        for fuente, destino, es_css in (
            (CSS_SOURCES, CSS_BUNDLE, True),
            (JS_SOURCES, JS_BUNDLE, False),
        ):
            contenido = self._build(base, fuente, es_css)
            ruta = os.path.join(base, destino.replace('/', os.sep))
            actual = None
            if os.path.exists(ruta):
                actual = io.open(ruta, encoding='utf-8', errors='replace').read()

            if actual == contenido:
                self.stdout.write('  = %-22s al dia (%d archivos, %.1f KB)' % (
                    destino, len(fuente), len(contenido.encode('utf-8')) / 1024))
                continue

            desactualizados.append(destino)
            if solo_comprobar:
                self.stdout.write(self.style.WARNING(
                    '  ! %-22s DESACTUALIZADO' % destino))
                continue

            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            io.open(ruta, 'w', encoding='utf-8', newline='\n').write(contenido)
            self.stdout.write(self.style.SUCCESS(
                '  v %-22s %d archivos -> %.1f KB' % (
                    destino, len(fuente), len(contenido.encode('utf-8')) / 1024)))

        if solo_comprobar and desactualizados:
            raise CommandError(
                'Bundles desactualizados: %s. Ejecute build_bundles.'
                % ', '.join(desactualizados))

    def _static_dir(self):
        """Carpeta de estaticos de origen, tanto en desarrollo como en produccion."""
        for ruta in list(getattr(settings, 'STATICFILES_DIRS', [])) + [settings.BASE_DIR / 'static']:
            if os.path.isdir(ruta):
                return str(ruta)
        raise CommandError('No se encontro la carpeta de estaticos.')

    def _build(self, base, rutas, es_css):
        partes = []
        for indice, rel in enumerate(rutas):
            ruta = os.path.join(base, rel.replace('/', os.sep))
            if not os.path.exists(ruta):
                raise CommandError('No existe %s' % ruta)
            texto = io.open(ruta, encoding='utf-8', errors='replace').read()

            if es_css:
                # @charset solo surte efecto si son los primerisimos bytes del
                # archivo, asi que se retira de todos y se emite una sola vez
                # al principio del bundle.
                texto = CHARSET_RE.sub('', texto, count=1)

            partes.append('/* %s */\n%s' % (rel, texto.strip()))

        # En JS se separa con ; por si algun archivo no termina en uno: sin
        # eso la insercion automatica de punto y coma puede unir sentencias.
        separador = '\n\n' if es_css else '\n;\n'
        cabecera = ('/* Generado por manage.py build_bundles. No editar a mano: '
                    'los originales son %s */\n' % ', '.join(rutas))
        # El CSS lleva caracteres no ASCII (flechas de menu en content:), que
        # se leerian mal sin la declaracion de codificacion al frente.
        prefijo = '@charset "utf-8";\n' if es_css else ''
        return prefijo + cabecera + separador.join(partes) + '\n'
