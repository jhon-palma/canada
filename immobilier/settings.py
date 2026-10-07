from pathlib import Path
from urllib.parse import urlsplit

from . import entorno

BASE_DIR = Path(__file__).resolve().parent.parent

# La configuracion viene de un .env. Mientras produccion no tenga el suyo se
# sigue aceptando el local_settings.py de antes, avisando; ver immobilier/entorno.py.
_ARCHIVO_ENV = entorno.cargar()
entorno.avisar_de_local_settings(_ARCHIVO_ENV)
if _ARCHIVO_ENV is None and entorno.hay_local_settings():
    from .local_settings import *  # noqa: F401,F403

SECRET_KEY = entorno.texto('SECRET_KEY', globals().get(
    'SECRET_KEY', 'django-insecure-46l99m0=n-fxom7f-7-q9ia8rt9-sh$c^vmz7dcjy9-#$v1j2w'))
FILE_CHARSET = 'utf-8'

# ---------------------------------------------------------------- del entorno
# Cada valor con su reserva en lo que trajera local_settings, para que la
# transicion no dependa del orden en que se suban los archivos.
DEBUG = entorno.booleano('DEBUG', globals().get('DEBUG', False))
SERVER = entorno.texto('SERVER', globals().get('SERVER', 'http://localhost:8000'))

NAME = entorno.texto('DB_NAME', globals().get('NAME', ''))
USER = entorno.texto('DB_USER', globals().get('USER', ''))
PASSWORD = entorno.texto('DB_PASSWORD', globals().get('PASSWORD', ''))
HOST = entorno.texto('DB_HOST', globals().get('HOST', '127.0.0.1'))
PORT = entorno.entero('DB_PORT', globals().get('PORT', 5432))

BASE_URL = entorno.texto('FOLLOWUPBOSS_BASE_URL',
                         globals().get('BASE_URL', 'https://api.followupboss.com/v1/'))
FOLLOWUPBOSS_API_KEY = entorno.texto('FOLLOWUPBOSS_API_KEY',
                                     globals().get('FOLLOWUPBOSS_API_KEY', ''))

KEY_API_YB = entorno.texto('YOUTUBE_API_KEY', globals().get('KEY_API_YB', ''))
CHANNEL_ID = entorno.texto('YOUTUBE_CHANNEL_ID', globals().get('CHANNEL_ID', ''))

AWS_S3_ACCESS_KEY_ID = entorno.texto('AWS_S3_ACCESS_KEY_ID',
                                     globals().get('AWS_S3_ACCESS_KEY_ID', ''))
AWS_S3_SECRET_ACCESS_KEY = entorno.texto('AWS_S3_SECRET_ACCESS_KEY',
                                         globals().get('AWS_S3_SECRET_ACCESS_KEY', ''))
AWS_STORAGE_BUCKET_NAME = entorno.texto('AWS_STORAGE_BUCKET_NAME',
                                        globals().get('AWS_STORAGE_BUCKET_NAME', ''))
AWS_S3_ENDPOINT_URL = entorno.texto('AWS_S3_ENDPOINT_URL',
                                    globals().get('AWS_S3_ENDPOINT_URL', ''))

# Las usa el importador de Centris para lanzar el script de descarga.
PYTHON = entorno.texto('PYTHON_BIN', globals().get('PYTHON', 'python3'))
PATH_BASE = entorno.texto('PATH_BASE', globals().get('PATH_BASE', str(BASE_DIR / 'data')))
PATH_BACKUP = entorno.texto('PATH_BACKUP', globals().get('PATH_BACKUP', PATH_BASE + '/backups'))

# Sin uso en el repositorio; se conservan por si los lee algo de fuera.
FTP_IP = entorno.texto('FTP_IP', globals().get('FTP_IP', ''))
FTP_USER = entorno.texto('FTP_USER', globals().get('FTP_USER', ''))
FTP_PASSWORD = entorno.texto('FTP_PASSWORD', globals().get('FTP_PASSWORD', ''))

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['www.ljrealties.com', 'ljrealties.com']

CSRF_TRUSTED_ORIGINS = ['https://www.ljrealties.com', 'https://ljrealties.com']

# Dominio canonico de robots.txt, sitemap.xml y las etiquetas og/absolutas.
# Se deriva de SERVER (local_settings) para tener una sola fuente de verdad:
# es el mismo valor que devuelve el filtro `server_url` en las plantillas.
_server = urlsplit(SERVER if '//' in SERVER else '//' + SERVER)
SITE_PROTOCOL = _server.scheme or ('http' if DEBUG else 'https')
SITE_DOMAIN = _server.netloc or ('localhost:8000' if DEBUG else 'www.ljrealties.com')
SITE_URL = '{}://{}'.format(SITE_PROTOCOL, SITE_DOMAIN)

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

# Estaticos y media. Esto estaba en local_settings.py, que no esta versionado:
# o sea que la decision de donde se guardan los archivos del sitio viajaba
# fuera del repositorio, maquina por maquina. No es configuracion -- no cambia
# por entorno mas alla del propio DEBUG -- sino logica, y le toca estar aqui.
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

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = []
    CORS_ALLOW_CREDENTIALS = False
else:
    _OPCIONES_SPACES = {
        'access_key': AWS_S3_ACCESS_KEY_ID,
        'secret_key': AWS_S3_SECRET_ACCESS_KEY,
        'bucket_name': AWS_STORAGE_BUCKET_NAME,
        'endpoint_url': AWS_S3_ENDPOINT_URL,
    }
    STORAGES = {
        'default': {
            'BACKEND': 'immobilier.storage.MediaS3Boto3Storage',
            'OPTIONS': dict(_OPCIONES_SPACES, querystring_auth=False, location='media'),
        },
        'staticfiles': {
            'BACKEND': 'storages.backends.s3.S3Storage',
            'OPTIONS': dict(_OPCIONES_SPACES, location='static', default_acl='public-read'),
        },
    }

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

# Los estaticos se sirven desde el edge del CDN de Spaces en vez del origen
# del bucket. Mismas rutas y mismos archivos, pero el edge responde en ~0,05s
# frente a ~0,95s del origen (esta en San Francisco) y anade
# Cache-Control: max-age=604800, que el origen no manda.
# Se aplica SOLO al almacenamiento staticfiles: el de media (las imagenes)
# se deja intacto a proposito, para que sus URLs sigan sin caducidad.
if not DEBUG and isinstance(globals().get('STORAGES'), dict):
    _spaces_region = urlsplit(AWS_S3_ENDPOINT_URL).netloc.split('.')[0]
    STATIC_CDN_DOMAIN = '{}.{}.cdn.digitaloceanspaces.com'.format(
        AWS_STORAGE_BUCKET_NAME, _spaces_region)
    _staticfiles = STORAGES.get('staticfiles')
    if _staticfiles is not None:
        _staticfiles.setdefault('OPTIONS', {})['custom_domain'] = STATIC_CDN_DOMAIN

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': NAME,
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': PORT,
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
USE_HTTPS = True

# --------- CONFIGURACION DE LENGUAJE ----------------

LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'America/Toronto'
USE_I18N = True
USE_TZ = True
USE_L10N = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
POSTS_PER_PAGE = 10


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
# CKEDITOR_5_CONFIGS = {
#     'default': {
#         'toolbar': ['heading', '|', 'bold', 'italic', 'link',
#                     'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],

#     },
#     'extends': {
#         'blockToolbar': [
#             'paragraph', 'heading1', 'heading2', 'heading3',
#             '|',
#             'bulletedList', 'numberedList',
#             '|',
#             'blockQuote',
#         ],
#         'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough', '|', 
#                     'bulletedList', 'numberedList', 'todoList', '|', 'fontSize', 'fontColor'],
        
#         'heading' : {
#             'options': [
#                 { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
#                 { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
#                 { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
#                 { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
#             ]
#         }
#     },
#     'list': {
#         'properties': {
#             'styles': 'true',
#             'startIndex': 'true',
#             'reversed': 'true',
#         } 
#     }
# }
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