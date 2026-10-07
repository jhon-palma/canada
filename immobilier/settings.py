import os
from pathlib import Path
from urllib.parse import urlsplit

import environ
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Toda la configuracion sale de un .env. Antes vivia en local_settings.py, un
# modulo de Python con las contrasenas escritas dentro que entraba aqui con
# `import *`: las credenciales en codigo fuente, mezcladas con la logica de los
# STORAGES, y sin forma de saber que definia cada archivo sin abrir los dos.
#
# Que archivo se lee, por orden: ENV_FILE si esta puesta, si no
# .env.<DJANGO_ENV> con 'dev' por defecto, si no .env. Lo que ya exista en el
# entorno del proceso manda sobre el archivo, que es lo que permite inyectar un
# secreto desde el panel del servidor sin dejarlo escrito en ningun sitio.
#
# Que el valor por defecto sea 'dev' no abre un agujero en produccion: los .env
# estan fuera de git, asi que en el servidor no hay ningun .env.dev que leer
# por descuido, y si alli se olvida DJANGO_ENV=prod el arranque se para en
# seco en vez de levantar con la configuracion de otro sitio.
env = environ.Env()

if os.environ.get('ENV_FILE'):
    _CANDIDATOS = [Path(os.environ['ENV_FILE'])]
else:
    _CANDIDATOS = [BASE_DIR / '.env.{}'.format(os.environ.get('DJANGO_ENV', 'dev')),
                   BASE_DIR / '.env']

_ARCHIVO_ENV = next((ruta for ruta in _CANDIDATOS if ruta.is_file()), None)
if _ARCHIVO_ENV is None:
    # Sin archivo no se arranca. Una configuracion a medias es peor: falla mas
    # tarde y mas lejos del motivo.
    raise ImproperlyConfigured(
        'No se encontro ningun archivo de configuracion. Se busco en: {}. Copia '
        '.env.example a .env.dev (o a .env.prod en el servidor) y rellenalo. En '
        'produccion acuerdate de DJANGO_ENV=prod.'.format(
            ', '.join(str(ruta) for ruta in _CANDIDATOS)))
env.read_env(_ARCHIVO_ENV)


DEBUG = env.bool('DEBUG', default=False)

# Firma las sesiones y los tokens CSRF. Obligatoria en los dos entornos y sin
# reserva: la que habia escrita en este archivo esta en el historial de git,
# asi que cualquiera con acceso al repositorio podia firmar sesiones validas.
SECRET_KEY = env.str('SECRET_KEY')

# Raiz publica del sitio. De aqui salen el dominio canonico de robots.txt y el
# sitemap, las URLs absolutas y las etiquetas og.
SERVER = env.str('SERVER')
_server = urlsplit(SERVER)
if not _server.scheme or not _server.netloc:
    raise ImproperlyConfigured(
        'SERVER tiene que ser una URL completa con esquema, como '
        'https://www.ljrealties.com, y vale {!r}.'.format(SERVER))
SITE_PROTOCOL = _server.scheme
SITE_DOMAIN = _server.netloc
SITE_URL = '{}://{}'.format(SITE_PROTOCOL, SITE_DOMAIN)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

# ---------------------------------------------------------------- base de datos
NAME = env.str('DB_NAME')
USER = env.str('DB_USER')
PASSWORD = env.str('DB_PASSWORD')
HOST = env.str('DB_HOST')
PORT = env.int('DB_PORT', default=5432)

# --------------------------------------------------------------- integraciones
BASE_URL = env.str('FOLLOWUPBOSS_BASE_URL', default='https://api.followupboss.com/v1/')
FOLLOWUPBOSS_API_KEY = env.str('FOLLOWUPBOSS_API_KEY', default='')

KEY_API_YB = env.str('YOUTUBE_API_KEY', default='')
CHANNEL_ID = env.str('YOUTUBE_CHANNEL_ID', default='')

# --------------------------------------------- almacenamiento en Spaces
# USE_SPACES decide donde viven los archivos del sitio, y es un eje propio: no
# se deduce de DEBUG. Se puede querer el bucket desde una maquina de desarrollo
# para reproducir un fallo de subida, o servir de disco en un entorno de
# pruebas con DEBUG ya apagado. Si esta encendido, las cuatro claves son
# obligatorias: vacias, los STORAGES se construirian igual y el fallo saldria
# al subir una foto, no al arrancar.
USE_SPACES = env.bool('USE_SPACES')

if USE_SPACES:
    AWS_S3_ACCESS_KEY_ID = env.str('AWS_S3_ACCESS_KEY_ID')
    AWS_S3_SECRET_ACCESS_KEY = env.str('AWS_S3_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = env.str('AWS_S3_ENDPOINT_URL')
else:
    AWS_S3_ACCESS_KEY_ID = ''
    AWS_S3_SECRET_ACCESS_KEY = ''
    AWS_STORAGE_BUCKET_NAME = ''
    AWS_S3_ENDPOINT_URL = ''

# --------------------------------------------------------------------- correo
# Las usa scripts/send_email.py, que las tenia escritas dentro junto con dos
# contrasenas de aplicacion de Gmail, en un archivo versionado.
EMAIL_HOST = env.str('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', default='')
# Con esto puesto, todo el correo va a esa direccion en vez de a su
# destinatario. Es lo que antes hacia la rama de DEBUG, pero dicho a proposito:
# en desarrollo se pone, en produccion se deja vacio.
EMAIL_REDIRECT_TO = env.str('EMAIL_REDIRECT_TO', default='')

# ------------------------------------------------ importador de fichas (Centris)
# PATH_BASE normalmente se deja sin poner: por defecto es la carpeta data/ del
# propio proyecto, que es donde deja los archivos scripts/download_data.py y
# resuelve bien en cualquier maquina. Ponerlo a mano en el .env fue lo que hizo
# que la configuracion de produccion llevase una ruta de Windows.
PYTHON = env.str('PYTHON_BIN', default='python3')
PATH_BASE = env.str('PATH_BASE', default=str(BASE_DIR / 'data'))

# Sin uso en el repositorio; se conservan por si los lee algo de fuera.
FTP_IP = env.str('FTP_IP', default='')
FTP_USER = env.str('FTP_USER', default='')
FTP_PASSWORD = env.str('FTP_PASSWORD', default='')

AUTH_USER_MODEL = 'accounts.CustomUser'
X_FRAME_OPTIONS = 'ALLOWALL'

INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.accounts',
    'apps.parametrization',
    'apps.properties',
    'apps.web',
    'apps.users',
    'related_admin',
    'apps.blog',
    'django_ckeditor_5',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'storages',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'apps.middleware.RedirigirURLsMezcladas',
    'apps.middleware.RevalidarHTML',
]

ROOT_URLCONF = 'immobilier.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'immobilier.wsgi.application'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Estaticos y media. Esto estaba en local_settings.py, que no se versionaba:
# o sea que la decision de donde se guardan los archivos del sitio viajaba
# fuera del repositorio, maquina por maquina. No es configuracion -- no cambia
# por entorno -- sino logica, y le toca estar aqui.
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# collectstatic no copia una carpeta: recoge lo que encuentran los finders, o
# sea STATICFILES_DIRS y las subcarpetas static/ de las apps instaladas.
# Ninguna app de este proyecto tiene una: los 2142 archivos del sitio viven en
# BASE_DIR/static, asi que esa carpeta tiene que ser una FUENTE en los dos
# entornos. Declararla solo como STATIC_ROOT -- que es el DESTINO -- hacia que
# collectstatic subiera los estaticos del admin y de terceros y ni uno del
# sitio, y por eso bundle.css y bundle.js acabaron en el repositorio en vez de
# en el bucket, dejando la portada sin hoja de estilos.
STATICFILES_DIRS = [BASE_DIR / 'static']

# FileSystemFinder aborta si STATIC_ROOT coincide con una entrada de
# STATICFILES_DIRS. Con el almacenamiento en Spaces collectstatic escribe en el
# bucket y STATIC_ROOT no llega a usarse, asi que se le da una ruta aparte para
# que los dos ajustes convivan.
STATIC_ROOT = BASE_DIR / '.staticfiles'

# URLs de S3 sin firmar. django-storages firma por defecto
# (AWS_QUERYSTRING_AUTH=True), y el almacenamiento staticfiles no lo
# declaraba, asi que cada CSS y JS salia como
# .../stylesheet.css?AWSAccessKeyId=...&Signature=...&Expires=...
# La firma cambia en cada renderizado, de modo que la URL cambia y ni el
# navegador ni ningun CDN podian cachear nada; ademas caduca en una hora.
# Requiere que los objetos del bucket sean public-read (ver el comando
# fix_static_acl). El almacenamiento de media ya lo declara en sus OPTIONS,
# asi que este ajuste no lo altera.
AWS_QUERYSTRING_AUTH = False

if USE_SPACES:
    # Los estaticos se sirven desde el edge del CDN de Spaces en vez del origen
    # del bucket. Mismas rutas y mismos archivos, pero el edge responde en
    # ~0,05s frente a ~0,95s del origen (esta en San Francisco) y anade
    # Cache-Control: max-age=604800, que el origen no manda. Solo los
    # estaticos: las imagenes se dejan en el origen a proposito, para que sus
    # URLs sigan sin caducidad.
    STATIC_CDN_DOMAIN = '{}.{}.cdn.digitaloceanspaces.com'.format(
        AWS_STORAGE_BUCKET_NAME, urlsplit(AWS_S3_ENDPOINT_URL).netloc.split('.')[0])

    _SPACES = {
        'access_key': AWS_S3_ACCESS_KEY_ID,
        'secret_key': AWS_S3_SECRET_ACCESS_KEY,
        'bucket_name': AWS_STORAGE_BUCKET_NAME,
        'endpoint_url': AWS_S3_ENDPOINT_URL,
    }
    STORAGES = {
        'default': {
            'BACKEND': 'immobilier.storage.MediaS3Boto3Storage',
            'OPTIONS': dict(_SPACES, querystring_auth=False, location='media'),
        },
        'staticfiles': {
            'BACKEND': 'storages.backends.s3.S3Storage',
            'OPTIONS': dict(_SPACES, location='static', default_acl='public-read',
                            custom_domain=STATIC_CDN_DOMAIN),
        },
    }

# sslmode a 'require' en produccion. La base esta en DigitalOcean y se llega a
# ella por internet; el valor por defecto de psycopg2 es 'prefer', que intenta
# cifrar pero acepta seguir en claro si el servidor no ofrece TLS, asi que una
# contrasena de administrador podria viajar sin cifrar sin que nada avise. En
# desarrollo se queda en 'prefer' porque el Postgres local no suele tener
# certificado.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': NAME,
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': PORT,
        'OPTIONS': {
            'sslmode': env.str('DB_SSLMODE', default='require'),
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',  # Backend de allauth
)


# -------- VARIABLES GLOBALES

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# --------- CONFIGURACION DE LENGUAJE ----------------

LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'America/Toronto'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --------- CONFIGURACION DE ARCHIVOS S3 ----------------

customColorPalette = [
    {
        'color': 'hsl(4, 90%, 58%)',
        'label': 'Red'
    },
    {
        'color': 'hsl(340, 82%, 52%)',
        'label': 'Pink'
    },
    {
        'color': 'hsl(291, 64%, 42%)',
        'label': 'Purple'
    },
    {
        'color': 'hsl(262, 52%, 47%)',
        'label': 'Deep Purple'
    },
    {
        'color': 'hsl(231, 48%, 48%)',
        'label': 'Indigo'
    },
    {
        'color': 'hsl(207, 90%, 54%)',
        'label': 'Blue'
    },
]

CKEDITOR_5_FILE_STORAGE = "apps.blog.storage.CustomStorage"
# La vista del paquete solo acepta la subida de un is_staff, y del equipo
# casi nadie lo es. apps.blog.ckeditor aplica el mismo permiso que el resto
# de la gestion del blog y reutiliza el resto de la maquinaria del paquete.
CK_EDITOR_5_UPLOAD_FILE_VIEW_NAME = "blog:ckeditor_upload"

# Este ajuste hace dos cosas a la vez: valida la extension en el servidor
# (FileExtensionValidator) y viaja al navegador como image.upload.types, que es
# lo que CKEditor consulta para decidir que archivos acepta. Un formato que no
# este aqui lo descarta el editor sin llegar a hacer la peticion, sin decir por
# que. Se deja fuera svg a proposito: es XML ejecutable y se guarda en un
# bucket publico.
CKEDITOR_5_UPLOAD_FILE_TYPES = ['jpeg', 'jpg', 'png', 'gif', 'webp', 'bmp', 'tiff']
# Ruta relativa, no '/static/...': forms.Media deja intacto lo que empieza por
# '/' y solo pasa por static() lo relativo. Con la ruta absoluta el editor
# pedia el CSS al propio dominio en vez de al CDN, y ahi responde 403.
CKEDITOR_5_CUSTOM_CSS = 'blog/css/editor.css'
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link','bulletedList', 'numberedList', 'blockQuote', 'imageUpload'],
        'contentsCss': ['https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700&display=swap', '/static/css/styles.css'],
        'bodyClass': 'ckeditor-custom',

    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
        'code','subscript', 'superscript', 'highlight', '|', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable',],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
            'tableProperties', 'tableCellProperties' ],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading' : {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
            ]
        }
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    }
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    },
}