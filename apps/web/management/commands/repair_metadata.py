"""Revisa y repara las filas de MetaDataWeb.

Cada pagina del sitio busca su fila por `origin` y hasta ahora lo hacia con
`objects.get()`, asi que una fila de menos daba DoesNotExist y una de mas
MultipleObjectsReturned: en los dos casos, un 500 de la pagina entera. Paso en
produccion con 'sell' (sin fila) y 'properties' (con dos), porque el formulario
de /metadata/ enviaba `origin` en un <select> oculto y al guardar reescribia la
clave de la fila.

Las vistas ya no se caen por esto, pero la fila sigue haciendo falta para que
el <title> y el <meta description> sean los correctos y no el texto de reserva.
Este comando dice que falta y que sobra, y lo arregla.

Uso:
    python manage.py repair_metadata                       # informe, no toca nada
    python manage.py repair_metadata --set <uuid> <origin> # devuelve una fila a su origin
    python manage.py repair_metadata --create <origin>     # crea una fila vacia
"""

from django.core.management.base import BaseCommand, CommandError

from apps.web.choices import WEB_META_ORIGIN_CHOICES
from apps.web.models import MetaDataWeb

ORIGENES = [clave for clave, _ in WEB_META_ORIGIN_CHOICES]


class Command(BaseCommand):
    help = 'Informa de los metadatos web que faltan o estan duplicados, y los repara.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--set', nargs=2, metavar=('UUID', 'ORIGIN'), dest='asignar',
            help='Cambia el origin de la fila indicada.')
        parser.add_argument(
            '--create', metavar='ORIGIN', dest='crear',
            help='Crea una fila vacia para ese origin.')

    def handle(self, *args, **options):
        if options['asignar']:
            return self._asignar(*options['asignar'])
        if options['crear']:
            return self._crear(options['crear'])
        self._informe()

    # -- informe ----------------------------------------------------------

    def _informe(self):
        filas = list(MetaDataWeb.objects.all().order_by('origin'))

        self.stdout.write('%-38s %-12s %s' % ('ID', 'ORIGIN', 'TITULO FR'))
        for fila in filas:
            self.stdout.write('%-38s %-12s %s' % (
                fila.id, fila.origin, (fila.m_title_f or '')[:60]))

        cuenta = {}
        for fila in filas:
            cuenta[fila.origin] = cuenta.get(fila.origin, 0) + 1

        faltan = [origen for origen in ORIGENES if origen not in cuenta]
        sobran = sorted(origen for origen, veces in cuenta.items() if veces > 1)
        huerfanos = sorted(origen for origen in cuenta if origen not in ORIGENES)

        self.stdout.write('')
        if faltan:
            self.stdout.write(self.style.ERROR(
                'Sin fila: %s' % ', '.join(faltan)))
            for origen in faltan:
                self.stdout.write(
                    '  python manage.py repair_metadata --create %s' % origen)
        if sobran:
            self.stdout.write(self.style.ERROR(
                'Duplicados: %s' % ', '.join(sobran)))
            self.stdout.write(
                '  Mira arriba cual de las filas repetidas es en realidad de otra'
                ' pagina y devuelvela a su sitio:')
            self.stdout.write(
                '  python manage.py repair_metadata --set <uuid> <origin>')
        if huerfanos:
            self.stdout.write(self.style.WARNING(
                'Con un origin que ya no existe en las opciones: %s'
                % ', '.join(huerfanos)))
        if not (faltan or sobran or huerfanos):
            self.stdout.write(self.style.SUCCESS(
                'Las %d filas estan bien: una por pagina.' % len(filas)))

    # -- reparacion -------------------------------------------------------

    def _asignar(self, uuid, origen):
        self._validar(origen)
        try:
            fila = MetaDataWeb.objects.get(id=uuid)
        except (MetaDataWeb.DoesNotExist, ValueError, TypeError):
            raise CommandError('No hay ninguna fila con el id %s.' % uuid)

        ocupada = MetaDataWeb.objects.filter(origin=origen).exclude(id=fila.id).first()
        if ocupada:
            raise CommandError(
                'El origin %s ya lo tiene la fila %s. Resuelve ese duplicado antes.'
                % (origen, ocupada.id))

        anterior, fila.origin = fila.origin, origen
        fila.save(update_fields=['origin'])
        self.stdout.write(self.style.SUCCESS(
            'Fila %s: %s -> %s' % (fila.id, anterior, origen)))

    def _crear(self, origen):
        self._validar(origen)
        if MetaDataWeb.objects.filter(origin=origen).exists():
            raise CommandError('Ya hay una fila con origin %s.' % origen)
        fila = MetaDataWeb.objects.create(origin=origen)
        self.stdout.write(self.style.SUCCESS(
            'Creada la fila %s con origin %s. Rellena sus textos en /metadata/.'
            % (fila.id, origen)))

    def _validar(self, origen):
        if origen not in ORIGENES:
            raise CommandError(
                '%s no es un origin valido. Los que hay: %s'
                % (origen, ', '.join(ORIGENES)))
