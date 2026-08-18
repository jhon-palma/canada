"""Convierte los banners de ImagesWeb a WebP.

Los 16 registros de ImagesWeb suman ~7,8 MB (contact_team.png solo pesa
4,4 MB) y son PNG/JPG a 1920px o mas. En WebP se reducen entre un 70% y un
90% sin diferencia perceptible, y como las plantillas los referencian por
{{ images.X.image.url }}, basta con reemplazar el archivo y guardar el
modelo: no hay que tocar ninguna plantilla.

Uso:
    python manage.py optimize_web_images              # simulacion, no escribe
    python manage.py optimize_web_images --apply      # convierte y guarda
    python manage.py optimize_web_images --apply --reference index_banner
"""

import io
import os

from PIL import Image

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from apps.web.models import ImagesWeb

MAX_WIDTH = 1920
QUALITY = 82


class Command(BaseCommand):
    help = 'Convierte las imagenes de ImagesWeb a WebP y las reescala a %dpx de ancho.' % MAX_WIDTH

    def add_arguments(self, parser):
        parser.add_argument(
            '--apply', action='store_true',
            help='Escribe los cambios. Sin este argumento solo simula.')
        parser.add_argument(
            '--delete-originals', action='store_true',
            help='Borra el archivo original tras convertir. Por defecto se '
                 'conserva para poder revertir.')
        parser.add_argument(
            '--reference', default=None,
            help='Convierte solo una referencia concreta (ej. index_banner).')
        parser.add_argument(
            '--quality', type=int, default=QUALITY,
            help='Calidad WebP, 1-100 (por defecto %d).' % QUALITY)
        parser.add_argument(
            '--max-width', type=int, default=MAX_WIDTH,
            help='Ancho maximo en pixeles (por defecto %d).' % MAX_WIDTH)

    def handle(self, *args, **options):
        apply_changes = options['apply']
        quality = options['quality']
        max_width = options['max_width']

        queryset = ImagesWeb.objects.all().order_by('reference')
        if options['reference']:
            queryset = queryset.filter(reference=options['reference'])

        if not queryset.exists():
            self.stderr.write('No hay imagenes que convertir.')
            return

        if not apply_changes:
            self.stdout.write(self.style.WARNING(
                'SIMULACION: no se escribe nada. Use --apply para confirmar.\n'))

        total_before = total_after = 0
        converted = skipped = failed = 0

        for item in queryset:
            name = item.image.name
            if not name:
                continue
            if name.lower().endswith('.webp'):
                self.stdout.write('  = %-26s ya esta en WebP' % item.reference)
                skipped += 1
                continue

            try:
                item.image.open('rb')
                original = item.image.read()
                item.image.close()
            except Exception as exc:
                self.stderr.write('  ! %-26s no se pudo leer: %s' % (item.reference, exc))
                failed += 1
                continue

            try:
                image = Image.open(io.BytesIO(original))
                # WebP no admite paleta ni CMYK; RGBA solo si hay transparencia real.
                if image.mode in ('P', 'LA'):
                    image = image.convert('RGBA' if 'transparency' in image.info else 'RGB')
                elif image.mode not in ('RGB', 'RGBA'):
                    image = image.convert('RGB')

                if image.width > max_width:
                    height = round(image.height * max_width / image.width)
                    image = image.resize((max_width, height), Image.LANCZOS)

                buffer = io.BytesIO()
                image.save(buffer, format='WEBP', quality=quality, method=6)
                data = buffer.getvalue()
            except Exception as exc:
                self.stderr.write('  ! %-26s fallo la conversion: %s' % (item.reference, exc))
                failed += 1
                continue

            before, after = len(original), len(data)
            if after >= before:
                self.stdout.write('  = %-26s WebP no mejora (%.1f KB), se deja igual'
                                  % (item.reference, before / 1024))
                skipped += 1
                continue

            total_before += before
            total_after += after
            converted += 1

            new_name = '%s.webp' % os.path.splitext(os.path.basename(name))[0]
            self.stdout.write('  %s %-26s %8.1f KB -> %7.1f KB  (-%.0f%%)  %s' % (
                'v' if apply_changes else '.', item.reference,
                before / 1024, after / 1024, 100 * (1 - after / before), new_name))

            if apply_changes:
                old_name = name
                item.image.save(new_name, ContentFile(data), save=True)
                # El original se conserva salvo peticion expresa: es la unica
                # via de vuelta si la conversion no convence.
                if options['delete_originals'] and item.image.name != old_name:
                    try:
                        item.image.storage.delete(old_name)
                    except Exception as exc:
                        self.stderr.write('    (no se pudo borrar %s: %s)' % (old_name, exc))

        self.stdout.write('')
        if converted:
            self.stdout.write(self.style.SUCCESS(
                '%d convertidas: %.2f MB -> %.2f MB (-%.0f%%, %.2f MB menos)' % (
                    converted, total_before / 1048576, total_after / 1048576,
                    100 * (1 - total_after / total_before),
                    (total_before - total_after) / 1048576)))
        if skipped:
            self.stdout.write('%d omitidas.' % skipped)
        if failed:
            self.stdout.write(self.style.ERROR('%d con error.' % failed))
        if converted and not apply_changes:
            self.stdout.write(self.style.WARNING(
                '\nNada se ha escrito. Repita con --apply para aplicarlo.'))
