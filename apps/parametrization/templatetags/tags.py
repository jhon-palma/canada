from django import template
from django.templatetags.static import static
from immobilier.settings import SERVER
from apps.estaticos import versionar
from apps.seo import absolute_url, alternate_path
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


@register.simple_tag
def static_v(ruta):
    """Como {% static %}, pero anadiendo ?v=<sha1 del contenido> a la URL.

    El porque de la marca, y por que el calculo vive en apps.estaticos y no
    aqui, esta explicado en ese modulo.
    """
    return versionar(static(ruta), ruta)
