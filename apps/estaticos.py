"""Version de contenido para los estaticos servidos desde el CDN.

Los estaticos salen del edge del CDN de Spaces con Cache-Control:
max-age=604800. Subir el archivo al bucket no invalida lo que el edge ya tiene
guardado: sigue entregando la copia vieja hasta que caducan los siete dias.
Purgar desde el panel es un paso manual, fuera del despliegue, y basta con que
falle o se olvide para que un arreglo de CSS no llegue a nadie durante una
semana -- que es exactamente lo que paso con el paginado del blog.

Con la version en la query cada contenido nuevo es una URL nueva, asi que el
edge la trata como un archivo que no tiene y la pide al origen. Se comprobo
contra produccion que esas URLs se siguen cacheando (primera peticion MISS,
segunda HIT), de modo que no se pierde el edge: solo se deja de depender de la
purga.

Vive aqui, y no en el tag de plantilla, porque publish_static tiene que
componer exactamente la misma URL para verificar lo que se sirve. Si cada uno
la calculase por su cuenta, la comprobacion podria dar por bueno un archivo que
el navegador nunca pide.
"""

import hashlib
import os

from django.contrib.staticfiles import finders

# Version calculada de cada estatico, para no releer el archivo en cada
# peticion. La clave lleva mtime y tamano, asi que un despliegue que cambie el
# archivo entra por una clave nueva y no hace falta reiniciar nada.
_VERSIONES = {}


def version(ruta):
    """sha1 corto del contenido del estatico, o None si no esta en disco.

    Es el sha1 y no la fecha para que la marca solo cambie cuando cambia el
    archivo de verdad: un despliegue que no toque el CSS no debe invalidar lo
    que el navegador ya tiene.
    """
    local = finders.find(ruta)
    if not local:
        return None

    try:
        estado = os.stat(local)
    except OSError:
        return None

    clave = (local, estado.st_mtime, estado.st_size)
    marca = _VERSIONES.get(clave)
    if marca is None:
        with open(local, 'rb') as archivo:
            marca = hashlib.sha1(archivo.read()).hexdigest()[:8]
        _VERSIONES[clave] = marca

    return marca


def versionar(url, ruta):
    """Anade ?v=<version> a una URL ya compuesta.

    Si el estatico no aparece en disco devuelve la URL tal cual: quedarse sin
    marca es preferible a quedarse sin hoja de estilos.
    """
    marca = version(ruta)
    if not marca:
        return url

    separador = '&' if '?' in url else '?'
    return '%s%sv=%s' % (url, separador, marca)
