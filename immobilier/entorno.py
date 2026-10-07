"""Lectura de la configuracion desde un archivo .env.

Antes esto vivia en immobilier/local_settings.py: un modulo de Python con las
contrasenas escritas dentro que settings.py importaba con `import *`. Tenia
tres problemas. Las credenciales estaban en codigo fuente, a un despiste de
acabar publicadas -- y no es un riesgo teorico: de las peticiones maliciosas
que recibe este sitio cada dia, una de cada cuatro va buscando justamente un
archivo con secretos. Mezclaba configuracion con logica, porque el mismo
archivo decidia tambien los STORAGES y las rutas de estaticos. Y al entrar con
`import *` no habia manera de saber que define cada cual sin abrir los dos.

Que archivo se lee, por orden:

1. ENV_FILE, si esta puesta: esa ruta exacta.
2. .env.<DJANGO_ENV>, con DJANGO_ENV a 'dev' si no se dice otra cosa. Asi
   conviven .env.dev y .env.prod en la misma maquina y en local no hace falta
   escribir la variable en cada comando.
3. .env

Las variables que ya existan en el entorno del proceso mandan sobre el
archivo, que es lo que permite inyectar un secreto desde el panel del servidor
sin dejarlo escrito en ningun sitio.

Si no aparece ninguno de esos archivos, el proyecto no arranca. Es a proposito:
una configuracion a medias es peor que no arrancar, porque falla mas tarde y
mas lejos del motivo.

Que el valor por defecto de DJANGO_ENV sea 'dev' no abre un agujero en
produccion: los .env estan fuera de git, asi que en el servidor no hay ningun
.env.dev que leer por descuido, y si alli se olvida DJANGO_ENV=prod el arranque
se para en seco en vez de levantar con la configuracion de otro sitio.
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

RAIZ = Path(__file__).resolve().parent.parent

_FALTA = object()

_AYUDA = (
    'Copia .env.example a .env.dev (o a .env.prod en el servidor) y rellenalo. '
    'En produccion acuerdate de DJANGO_ENV=prod.'
)


def _candidatos():
    """Las rutas donde se busca el archivo, en orden de preferencia."""
    explicito = os.environ.get('ENV_FILE')
    if explicito:
        return [Path(explicito)]
    nombre = os.environ.get('DJANGO_ENV', 'dev')
    return [RAIZ / '.env.{}'.format(nombre), RAIZ / '.env']


def cargar():
    """Mete en os.environ lo que haya en el archivo y devuelve su ruta.

    No pisa lo que ya este definido: el entorno del proceso tiene prioridad.
    """
    rutas = _candidatos()
    ruta = next((r for r in rutas if r.is_file()), None)
    if ruta is None:
        raise ImproperlyConfigured(
            'No se encontro ningun archivo de configuracion. Se busco en: {}. {}'.format(
                ', '.join(str(r) for r in rutas), _AYUDA))

    with ruta.open(encoding='utf-8') as archivo:
        for numero, linea in enumerate(archivo, 1):
            linea = linea.strip()
            if not linea or linea.startswith('#'):
                continue
            if linea.startswith('export '):
                linea = linea[len('export '):].lstrip()
            if '=' not in linea:
                raise ImproperlyConfigured(
                    '{}, linea {}: se esperaba CLAVE=valor.'.format(ruta.name, numero))
            clave, _, valor = linea.partition('=')
            valor = valor.strip()
            # Las comillas sirven para que un valor pueda llevar espacios al
            # principio o al final; no forman parte del valor.
            if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in '\'"':
                valor = valor[1:-1]
            os.environ.setdefault(clave.strip(), valor)

    return ruta


def texto(clave, defecto=_FALTA):
    valor = os.environ.get(clave)
    if valor is None or valor == '':
        if defecto is _FALTA:
            raise ImproperlyConfigured(
                'Falta {} en la configuracion. {}'.format(clave, _AYUDA))
        return defecto
    return valor


def entero(clave, defecto=_FALTA):
    valor = texto(clave, defecto if defecto is _FALTA else str(defecto))
    try:
        return int(valor)
    except (TypeError, ValueError):
        raise ImproperlyConfigured(
            '{} tiene que ser un numero, y vale {!r}.'.format(clave, valor))


def booleano(clave, defecto=_FALTA):
    valor = texto(clave, defecto if defecto is _FALTA else ('true' if defecto else 'false'))
    valor = str(valor).strip().lower()
    if valor in ('1', 'true', 'yes', 'on', 'si'):
        return True
    if valor in ('0', 'false', 'no', 'off'):
        return False
    raise ImproperlyConfigured(
        '{} tiene que ser true o false, y vale {!r}.'.format(clave, valor))
