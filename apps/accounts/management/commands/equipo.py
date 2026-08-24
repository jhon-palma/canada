"""Da y quita el permiso de gestion interna (is_staff) a una cuenta.

is_staff es lo que en este proyecto separa al equipo de un visitante
registrado, y hace falta en tres sitios a la vez:

  - las vistas de gestion del blog (crear, editar, activar articulos),
  - la subida de imagenes dentro del editor, que django_ckeditor_5 solo acepta
    de un usuario con is_staff,
  - la vista previa de un articulo programado antes de su fecha.

El blog tiene registro publico: signup_blog crea un CustomUser y le inicia la
sesion, asi que estar autenticado no distingue a nadie. De ahi que la llave
sea is_staff y no "haber iniciado sesion".

Uso:
    python manage.py equipo                          # lista las cuentas activas
    python manage.py equipo --alta correo@ejemplo    # se lo concede
    python manage.py equipo --baja correo@ejemplo    # se lo retira

--alta y --baja aceptan varios correos separados por espacios.
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

Usuario = get_user_model()


class Command(BaseCommand):
    help = 'Lista, concede o retira is_staff (permiso de gestion interna).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--alta', nargs='+', metavar='CORREO',
            help='Concede is_staff a esas cuentas.')
        parser.add_argument(
            '--baja', nargs='+', metavar='CORREO',
            help='Retira is_staff de esas cuentas.')

    def handle(self, *args, **options):
        if options['alta']:
            self._cambiar(options['alta'], True)
        if options['baja']:
            self._cambiar(options['baja'], False)
        self._listar()

    def _cambiar(self, correos, valor):
        encontrados = Usuario.objects.filter(email__in=correos)
        faltan = set(correos) - set(encontrados.values_list('email', flat=True))
        if faltan:
            raise CommandError(
                'No hay ninguna cuenta con estos correos: %s' % ', '.join(sorted(faltan)))

        for cuenta in encontrados:
            if cuenta.is_staff == valor:
                self.stdout.write('  %-36s ya estaba %s' % (
                    cuenta.email, 'de alta' if valor else 'de baja'))

        cambiadas = encontrados.exclude(is_staff=valor).update(is_staff=valor)
        self.stdout.write(self.style.SUCCESS(
            '%d cuenta(s) %s.' % (cambiadas, 'dadas de alta' if valor else 'dadas de baja')))

    def _listar(self):
        cuentas = Usuario.objects.filter(is_active=True).order_by('email')
        self.stdout.write('')
        self.stdout.write('%-38s %s' % ('CUENTA ACTIVA', 'PUEDE GESTIONAR'))
        for cuenta in cuentas:
            self.stdout.write('%-38s %s' % (
                cuenta.email, 'si' if cuenta.is_staff else '-'))

        con_permiso = sum(1 for c in cuentas if c.is_staff)
        self.stdout.write('')
        if not con_permiso:
            self.stdout.write(self.style.ERROR(
                'Ninguna cuenta puede gestionar el blog. Concedeselo a alguien '
                'con --alta antes de desplegar, o el equipo se queda fuera.'))
        else:
            self.stdout.write('%d de %d cuentas pueden gestionar.' % (con_permiso, len(cuentas)))
