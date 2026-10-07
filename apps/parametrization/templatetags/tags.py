from django import template
from django.templatetags.static import static
from immobilier.settings import SERVER
from apps.estaticos import versionar
from apps.seo import absolute_url, alternate_path, canonical_path, normalize_language
import ast, json


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

    Devuelve la ruta limpia y canonica, sin cadena de consulta, porque el
    mismo valor alimenta las etiquetas hreflang del head, y ahi un ?page= o un
    ?popup= no pintan nada. El enlace visible le pega la consulta por su
    cuenta, que es el unico sitio donde hace falta.
    """
    request = context.get('request')
    if request is None:
        return '/%s/' % target_language
    extra = [(current_slug, translated_slug)] if current_slug and translated_slug else None
    return canonical_path(alternate_path(request.path, target_language, extra_slugs=extra))


@register.simple_tag(takes_context=True)
def canonical_url(context):
    """URL absoluta y canonica de la pagina que se esta sirviendo.

    Conserva `page` y solo `page`: la pagina 2 de un listado no es un
    duplicado de la 1 -- lleva otras fichas --, y apuntar su canonical a la 1
    le diria a Google que no indexe lo que hay en ella. El resto de
    parametros, popup o utm, no cambian el contenido y se quedan fuera.
    """
    request = context.get('request')
    if request is None:
        return absolute_url('/')
    ruta = canonical_path(request.path)
    pagina = request.GET.get('page')
    if pagina and pagina != '1':
        ruta = '{}?page={}'.format(ruta, pagina)
    return absolute_url(ruta)


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


@register.simple_tag
def static_v(ruta):
    """Como {% static %}, pero anadiendo ?v=<sha1 del contenido> a la URL.

    El porque de la marca, y por que el calculo vive en apps.estaticos y no
    aqui, esta explicado en ese modulo.
    """
    return versionar(static(ruta), ruta)


@register.simple_tag
def inicio_path(language=None):
    """Ruta de la portada del idioma, ya canonica.

    La portada francesa vive en / y en /fr/, y una de las dos redirige a la
    otra. Los enlaces internos -- el logo de la cabecera, el del pie, las
    salidas del 404 -- apuntaban a /<idioma>/ a secas, asi que la mitad de la
    navegacion del sitio pasaba por un 301 innecesario y Google veia cientos
    de enlaces internos a una URL que redirige.
    """
    return canonical_path('/{}/'.format(normalize_language(language)))


@register.simple_tag(takes_context=True)
def alternate_canonical(context, ruta_alterna):
    """URL absoluta del equivalente en el otro idioma, con la misma pagina.

    Las anotaciones hreflang tienen que ser reciprocas: si la pagina 2 en
    frances declara el ingles, el ingles que declare tiene que ser tambien la
    2, o Google descarta el par. Sin esto la 2 francesa apuntaba a la 1
    inglesa y la 1 inglesa a la 1 francesa.
    """
    request = context.get('request')
    pagina = request.GET.get('page') if request is not None else None
    if pagina and pagina != '1':
        ruta_alterna = '{}?page={}'.format(ruta_alterna, pagina)
    return absolute_url(ruta_alterna)
