from django import template
# from config.settings import STATIC_URL, SERVER, MEDIA_URL
from immobilier.settings import SERVER
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