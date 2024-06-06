from django.core.cache import cache
from ..parametrization.dates.utils import *

import re,  json, ast

def check_cell(cell):
    number = filter(lambda x: x.isdigit(), cell)
    str_number = number.replace(r' ', '')
    if len(str_number) in [11,12]:
        indicative = number[0:2]
        number = str_number[2:len(str_number)]
    return number


def chat_id(indicative, number):
    chat_id = ''
    if len(number) == 9:
        chat_id = '{}{}@c.us'.format(indicative, number)
    if len(number) == 10:
        chat_id = '{}{}@c.us'.format(57, number)
    return chat_id


def check_email(email):  
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,email)):  
        return email
    else:  
        return ''
        

def get_filters_request(dict_filters, list_filters_in):
    filters = {}
    for f in dict_filters:
        if '__exclude' not in f:
            value = dict_filters.get(f)
            if f not in list_filters_in:
                if len(value) > 1:
                    f = '{}__contains'.format(f)
                    value = ','.join(value)
                else:
                    value = value[0]
                    if '__isnull' in f:
                        value = ast.literal_eval(value)
                    if '__range' in f:
                        date = ''.join(value)
                        value = date.split(',')
            filters[f] = value
    clean = dict_clean(filters)
    return clean


def dict_clean(dict):
    list_clear = [None,'',['']]
    for k, v in dict.items():
        if v in list_clear or k in list_clear:
            del dict[k]

    str = json.dumps(dict)
    dict = ast.literal_eval(str)
    return dict


def get_type_propertie(typpe):
    if typpe in range(1,9):
        type_propertie = 'departament'
    if typpe in range(9,14):
        type_propertie = 'house'
    if typpe == 14:
        type_propertie = 'office'
    if typpe == 15:
        type_propertie = 'hotel'
    if typpe == 16:
        type_propertie = 'comercial'
    if typpe == 17:
        type_propertie = 'industrial'
    if typpe in [18, 19]:
        type_propertie = 'terrain'
    if typpe == 20:
        type_propertie = 'other'
    return type_propertie


def get_offices(region):
    key = 'api-offices-region-{}'.format(region)
    in_cache = data_in_cache(key)

    if not in_cache:
        url = '{}office/region/{}'.format(URL_API, region)
        response = requests.get(url).json()
        in_cache = cache.set(key, response, timeout=3000)
        return in_cache
    else:
        return in_cache


def data_in_cache(key):
    data = cache.get(key)
    if data != None:
        return data
    else:
        return False


def remove_spaces(string, pattern):
    sentence = re.sub(pattern, '', string)
    return sentence


def removeKey(dict, remove):
    for key in remove:
        try: del dict[key]
        except: pass
    return dict


def del_none_keys(dict):
    for elem in dict.keys():
        if dict[elem] == None or dict[elem] == '':
            del dict[elem]
    return dict


def dict_clean(dict):
    list_clear = [None, '', 'csrfmiddlewaretoken', 'paginate','page']
    for k, v in dict.items():
        if v in list_clear or k in list_clear:
            del dict[k]
    return dict

def get_filters_request(dict_filters, list_filters_in):
    filters = {}
    for f in dict_filters:
        if '__exclude' not in f:
            value = dict_filters.get(f)
            if f not in list_filters_in:
                if len(value) > 1:
                    f = '{}__contains'.format(f)
                    value = ','.join(value)
                else:
                    value = value[0]
                    if '__isnull' in f:
                        value = ast.literal_eval(value)
                    if '__range' in f:
                        date = ''.join(value)
                        value = date.split(',')
            filters[f] = value
    clean = dict_clean(filters)
    return clean
