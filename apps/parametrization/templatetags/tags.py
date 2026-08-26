from django import template
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from immobilier.settings import SERVER
from apps.seo import absolute_url, alternate_path
import ast, hashlib, json, os


register = template.Library()

@register.simple_tag
def define(val=None):
  return val


@register.filter
def get_item(dictionary, key):
    dict = json.loads(dictionary)
    return dict.get(key)


@register.filter
def server_url(server):
    return SERVER


@register.filter
def absolute(path):
    """Convierte una ruta relativa en absoluta sobre el dominio canonico."""
    return absolute_url(path)


@register.simple_tag(takes_context=True)
def alternate_url(context, target_language, current_slug=None, translated_slug=None):
    """href de la misma pagina en el otro idioma.

    El selector de idioma solo tenia onclick, asi que Google no podia
    seguirlo y no descubria la version en el otro idioma.
    """
    request = context.get('request')
    if request is None:
        return '/%s/' % target_language
    extra = [(current_slug, translated_slug)] if current_slug and translated_slug else None
    return alternate_path(request.path, target_language, extra_slugs=extra)


@register.filter
def key_maps(maps):
    return None


@register.filter
def format_money(value):
    if value not in ['',0,None]:
        try:
            s = '{:.2f}'.format(float(value))
            i = s.index('.')
            while i > 3:
                i = i - 3
                s = s[:i] + ',' + s[i:]
            return s
        except:
            l = list(value)
            i = value.index('.') + 3
            return(''.join(l[:i]))
    else:
        return ('0')


@register.filter
def concat(value, concact):
    if value != '':
        if concact == '%':
            return '{}{}'.format(value, concact)
        else:
            return '{} {}'.format(value, concact)
    else:
        return ''


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def format_number(value):
    try:
        value = float(value)
        return '{:,.0f}'.format(value).replace(',', ' ')
    except (ValueError, TypeError):
        return value
    
    
@register.filter
def tag_in_list(value, list):
    if_list = list.split(',')
    return True if value in if_list else False


@register.filter
def multiply(value, arg):
    try:
        value_str = str(value).replace(',', '.')
        return float(value_str) * float(arg)
    except (ValueError, TypeError):
        return ''


# Version calculada de cada estatico, para no releer el archivo en cada
# peticion. La clave lleva mtime y tamano, asi que un despliegue que cambie el
# archivo entra por una clave nueva y no hace falta reiniciar nada.
_VERSIONES = {}


@register.simple_tag
def static_v(ruta):
    """Como {% static %}, pero anadiendo ?v=<sha1> a la URL.

    Los estaticos se sirven desde el edge del CDN de Spaces con
    Cache-Control: max-age=604800. Subir el archivo al bucket no invalida lo
    que el edge ya tiene guardado: sigue entregando la copia vieja hasta que
    caducan los siete dias. Purgar desde el panel es un paso manual, fuera del
    despliegue, y basta con que falle o se olvide para que un arreglo de CSS no
    llegue a nadie durante una semana -- que es exactamente lo que paso con el
    paginado del blog.

    Con la version en la query cada contenido nuevo es una URL nueva, asi que
    el edge la trata como un archivo que no tiene y la pide al origen. Se
    comprobo contra produccion que esas URLs se siguen cacheando (primera
    peticion MISS, segunda HIT), de modo que no se pierde el edge: solo se deja
    de depender de la purga.

    La marca es el sha1 del contenido, no la fecha, para que solo cambie cuando
    cambia el archivo de verdad. Si el estatico no aparece en disco se devuelve
    la URL tal cual: quedarse sin marca es peor que quedarse sin hoja de
    estilos.
    """
    url = static(ruta)

    local = finders.find(ruta)
    if not local:
        return url

    try:
        estado = os.stat(local)
    except OSError:
        return url

    clave = (local, estado.st_mtime, estado.st_size)
    version = _VERSIONES.get(clave)
    if version is None:
        with open(local, 'rb') as archivo:
            version = hashlib.sha1(archivo.read()).hexdigest()[:8]
        _VERSIONES[clave] = version

    separador = '&' if '?' in url else '?'
    return '%s%sv=%s' % (url, separador, version)
