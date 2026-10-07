"""Lectura de la configuracion desde un archivo .env.

Antes todo esto vivia en immobilier/local_settings.py: un modulo de Python con
las contrasenas escritas dentro que settings.py importaba con `import *`. Tenia
tres problemas. Las credenciales estaban en codigo fuente, a un despiste de
acabar en git -- y el sitio recibe cada dia miles de peticiones que van
buscando justamente un archivo con secretos. Mezclaba configuracion con logica,
porque el mismo archivo decidia tambien los STORAGES y las rutas de estaticos.
Y al ser `import *` no habia manera de saber que define cada cual sin abrir los
dos archivos.

Que archivo se lee, por orden:

1. ENV_FILE, si esta puesta: esa ruta exacta.
2. .env.<DJANGO_ENV>, con DJANGO_ENV a 'dev' si no se dice otra cosa. Asi
   conviven .env.dev y .env.prod en la misma maquina y en local no hace falta
   escribir la variable en cada comando.
3. .env

Que el valor por defecto sea 'dev' no es un riesgo para produccion: los
archivos .env estan fuera de git, asi que en el servidor no hay ningun
.env.dev que leer por descuido. Si alguien olvida DJANGO_ENV=prod alli, no
encuentra archivo y falla a la vista en vez de arrancar con la configuracion
equivocada.

Las variables que ya existan en el entorno del proceso mandan sobre el archivo,
que es lo que permite inyectar un secreto desde el panel del servidor sin
tocar ningun archivo.

Si no aparece ninguno de esos archivos pero si local_settings.py, se usa ese y
se avisa por stderr. Es a proposito: el sitio esta en produccion y un
despliegue no puede quedarse sin configuracion por el orden en que se suban
los archivos. Cuando produccion tenga su .env, local_settings.py se puede
borrar y esa rama desaparece.
"""

import os
import sys
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

RAIZ = Path(__file__).resolve().parent.parent

_FALTA = object()


def _ruta_del_archivo():
    """El .env que toca leer, o None si no hay ninguno."""
    explicito = os.environ.get('ENV_FILE')
    if explicito:
        return Path(explicito)

    entorno = os.environ.get('DJANGO_ENV', 'dev')
    candidatos = [RAIZ / '.env.{}'.format(entorno), RAIZ / '.env']

    for candidato in candidatos:
        if candidato.is_file():
            return candidato
    return None


def cargar():
    """Mete en os.environ lo que haya en el archivo. Devuelve su ruta o None.

    No pisa lo que ya este definido: el entorno del proceso tiene prioridad.
    """
    ruta = _ruta_del_archivo()
    if ruta is None:
        return None
    if not ruta.is_file():
        raise ImproperlyConfigured('ENV_FILE apunta a {}, que no existe.'.format(ruta))

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
            clave = clave.strip()
            valor = valor.strip()
            # Las comillas son para que un valor pueda llevar espacios al
            # principio o al final; no forman parte del valor.
            if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in '\'"':
                valor = valor[1:-1]
            os.environ.setdefault(clave, valor)

    return ruta


def hay_local_settings():
    return (RAIZ / 'immobilier' / 'local_settings.py').is_file()


def avisar_de_local_settings(ruta_env):
    """Un aviso por stderr si se sigue tirando del modulo antiguo."""
    if ruta_env is None and hay_local_settings():
        sys.stderr.write(
            'AVISO: no se encontro ningun .env y se esta usando '
            'immobilier/local_settings.py. Copia .env.example a .env, '
            'rellenalo y borra local_settings.py.\n')


def texto(clave, defecto=_FALTA):
    valor = os.environ.get(clave)
    if valor is None or valor == '':
        if defecto is _FALTA:
            raise ImproperlyConfigured(
                'Falta {} en el .env (ni en el entorno del proceso).'.format(clave))
        return defecto
    return valor


def entero(clave, defecto=_FALTA):
    valor = texto(clave, defecto if defecto is _FALTA else str(defecto))
    try:
        return int(valor)
    except (TypeError, ValueError):
        raise ImproperlyConfigured('{} tiene que ser un numero, y vale {!r}.'.format(clave, valor))


def booleano(clave, defecto=_FALTA):
    valor = texto(clave, defecto if defecto is _FALTA else ('true' if defecto else 'false'))
    valor = str(valor).strip().lower()
    if valor in ('1', 'true', 'yes', 'on', 'si'):
        return True
    if valor in ('0', 'false', 'no', 'off'):
        return False
    raise ImproperlyConfigured(
        '{} tiene que ser true o false, y vale {!r}.'.format(clave, valor))
