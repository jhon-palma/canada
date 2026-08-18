"""Pone en public-read los estaticos del bucket que quedaron privados.

Parte de los CSS se subio sin el ACL public-read, asi que django-storages
no puede servirlos con una URL limpia y recurre a URLs firmadas
(?AWSAccessKeyId=...&Signature=...&Expires=...). Eso tiene tres costes:

  - La firma cambia en cada renderizado, de modo que la URL cambia y ni el
    navegador ni ningun CDN pueden cachear nunca el archivo.
  - La firma caduca (por defecto en una hora): una pagina abierta o cacheada
    mas tiempo se queda sin CSS.
  - Obliga a servir desde el origen del bucket, no desde el edge.

Una vez todo es publico se puede anadir "querystring_auth": False al
almacenamiento staticfiles de local_settings.py y las URLs quedan limpias y
cacheables. Hazlo en este orden: primero los permisos, luego la opcion; al
reves el sitio se queda sin estilos.

Uso:
    python manage.py fix_static_acl              # simulacion, no escribe
    python manage.py fix_static_acl --apply
    python manage.py fix_static_acl --prefix static/web/css/ --apply
"""

import boto3

from django.core.management.base import BaseCommand, CommandError

PUBLIC_URI = 'http://acs.amazonaws.com/groups/global/AllUsers'


class Command(BaseCommand):
    help = 'Marca como public-read los objetos privados del prefijo static/ en el bucket.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--apply', action='store_true',
            help='Escribe los cambios. Sin este argumento solo simula.')
        parser.add_argument(
            '--prefix', default='static/',
            help='Prefijo a revisar (por defecto static/).')

    def handle(self, *args, **options):
        try:
            from immobilier.local_settings import (
                AWS_S3_ACCESS_KEY_ID, AWS_S3_SECRET_ACCESS_KEY,
                AWS_STORAGE_BUCKET_NAME, AWS_S3_ENDPOINT_URL,
            )
        except ImportError as exc:
            raise CommandError('Faltan las credenciales de S3 en local_settings: %s' % exc)

        apply_changes = options['apply']
        prefix = options['prefix']

        s3 = boto3.client(
            's3',
            endpoint_url=AWS_S3_ENDPOINT_URL,
            aws_access_key_id=AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY,
        )

        if not apply_changes:
            self.stdout.write(self.style.WARNING(
                'SIMULACION: no se escribe nada. Use --apply para confirmar.\n'))

        revisados = privados = corregidos = fallidos = 0
        paginador = s3.get_paginator('list_objects_v2')

        for pagina in paginador.paginate(Bucket=AWS_STORAGE_BUCKET_NAME, Prefix=prefix):
            for obj in pagina.get('Contents', []):
                key = obj['Key']
                if key.endswith('/'):
                    continue
                revisados += 1
                try:
                    acl = s3.get_object_acl(Bucket=AWS_STORAGE_BUCKET_NAME, Key=key)
                except Exception as exc:
                    self.stderr.write('  ! %-60s no se pudo leer: %s' % (key[-60:], exc))
                    fallidos += 1
                    continue

                es_publico = any(
                    (g.get('Grantee') or {}).get('URI') == PUBLIC_URI
                    for g in acl.get('Grants', [])
                )
                if es_publico:
                    continue

                privados += 1
                self.stdout.write('  %s %s' % ('v' if apply_changes else '.', key))

                if apply_changes:
                    try:
                        s3.put_object_acl(
                            Bucket=AWS_STORAGE_BUCKET_NAME, Key=key, ACL='public-read')
                        corregidos += 1
                    except Exception as exc:
                        self.stderr.write('    error: %s' % exc)
                        fallidos += 1

        self.stdout.write('')
        self.stdout.write('%d objetos revisados, %d privados.' % (revisados, privados))
        if apply_changes:
            self.stdout.write(self.style.SUCCESS('%d marcados como publicos.' % corregidos))
        elif privados:
            self.stdout.write(self.style.WARNING(
                'Nada se ha escrito. Repita con --apply para aplicarlo.'))
        if fallidos:
            self.stdout.write(self.style.ERROR('%d con error.' % fallidos))
