"""Helpers compartidos para URLs canonicas y idioma.

El sitio es bilingue con el idioma como segmento de la URL (``/fr/...`` y
``/en/...``), no con los prefijos i18n de Django, y no usa LocaleMiddleware.
Estas utilidades centralizan las dos cosas que de ahi se derivan: normalizar
el idioma activo y construir URLs absolutas sobre el dominio canonico.
"""

from django.conf import settings
from django.utils.translation import get_language
from types import SimpleNamespace

LANGUAGES = ['fr', 'en']
DEFAULT_LANGUAGE = LANGUAGES[0]


def normalize_language(language):
    """Reduce cualquier codigo de idioma a 'fr' o 'en'.

    Acepta variantes regionales ('fr-FR', 'en-CA') y None.
    """
    if not language:
        return DEFAULT_LANGUAGE
    language = str(language).lower().split('-')[0]
    return language if language in LANGUAGES else DEFAULT_LANGUAGE


def current_language():
    """Idioma activo normalizado a 'fr' o 'en'."""
    return normalize_language(get_language())


def site_domain():
    """Dominio canonico (con puerto si aplica), sin esquema."""
    return settings.SITE_DOMAIN


def site_url():
    """Raiz canonica del sitio, sin barra final. Ej: https://www.ljrealties.com"""
    return settings.SITE_URL


def absolute_url(path):
    """Convierte una ruta relativa en absoluta sobre el dominio canonico."""
    return '{}{}'.format(site_url(), path)


# Pares de slug equivalentes entre idiomas. Es la misma tabla que usa
# changeParameterInURL() en static/app/js/functions/master.js; se replica
# aqui para poder emitir el enlace real en el HTML y no solo por JavaScript.
SLUG_TRANSLATIONS = [
    ('proprietes', 'properties'),
    ('propriete', 'propertie'),
    ('proprietes-a-vendre', 'properties-for-sale'),
    ('proprietes-a-louer', 'properties-for-rent'),
    ('courtier-immobilier', 'real-estate-broker'),
    ('acheter', 'buying'),
    ('vendre', 'selling'),
    ('contact-courtier-immobilier', 'contact-realestate-broker'),
    ('politique-confidentialite', 'privacy-policy'),
]


def alternate_path(path, target_language, extra_slugs=None):
    """Ruta equivalente a `path` en el otro idioma.

    Sustituye el segmento de idioma y los slugs traducibles. `extra_slugs`
    permite anadir pares (actual, traducido) propios de la pagina, como el
    slug de un articulo del blog.

    Se usa para dar un href real al selector de idioma: sin el, Google no
    puede seguir el enlace y no descubre la version en el otro idioma.
    """
    target_language = normalize_language(target_language)
    source_language = 'en' if target_language == 'fr' else 'fr'

    pares = list(extra_slugs or [])
    for fr, en in SLUG_TRANSLATIONS:
        pares.append((fr, en) if target_language == 'en' else (en, fr))
    pares.append((source_language, target_language))

    nueva = path
    for actual, traducido in pares:
        if actual and traducido:
            nueva = nueva.replace('/%s/' % actual, '/%s/' % traducido)

    # La portada se sirve tanto en / como en /<lang>/.
    if nueva == path and '/%s/' % target_language not in nueva:
        nueva = '/%s/' % target_language
    return nueva


MARCA = 'LJ Realties'


def meta_de_landing(fila, tipo, cantidad):
    """Titulo, descripcion y encabezado propios de una landing de busqueda.

    Todas las landings cargaban MetaDataWeb.for_origin('properties'), de modo
    que las de La Prairie, LaSalle, Laval y las demas compartian titulo,
    descripcion y encabezado: cientos de paginas que, por lo que declaraban de
    si mismas, eran la misma. Eso es lo que hacia inutil anadirles texto --
    por bueno que fuese, seguian presentandose como paginas identicas.

    Devuelve los cuatro campos que lee header_web.html, que solo los usa si
    estan los cuatro, mas los dos encabezados. El nombre sale del propio dato:
    la descripcion del municipio, que es unica, o la de la categoria en cada
    idioma.
    """
    if tipo == 'quartier':
        nombre_fr = nombre_en = (fila.description or '').strip()
        encabezado_fr = 'Maisons à vendre à {}'.format(nombre_fr)
        encabezado_en = 'Homes for sale in {}'.format(nombre_en)
        donde_fr, donde_en = 'à {}'.format(nombre_fr), 'in {}'.format(nombre_en)
        que_fr, que_en = 'propriétés', 'properties'
    else:
        nombre_fr = (fila.description_francaise or '').strip()
        nombre_en = (fila.description_anglaise or '').strip()
        encabezado_fr = '{} à vendre à Montréal'.format(nombre_fr)
        encabezado_en = '{} for sale in Montreal'.format(nombre_en)
        donde_fr, donde_en = 'dans la région de Montréal', 'in the Montreal area'
        que_fr, que_en = nombre_fr.lower(), nombre_en.lower()

    # La cuenta va en la descripcion porque es el dato que distingue de verdad
    # una landing de otra. Si no hay fichas se omite en vez de escribir un
    # cero, que invita a no entrar.
    if cantidad:
        descripcion_fr = '{} {} à vendre {}. Photos, prix et visites avec {}, courtiers immobiliers à Montréal.'.format(
            cantidad, que_fr, donde_fr, MARCA)
        descripcion_en = '{} {} for sale {}. Photos, prices and viewings with {}, real estate brokers in Montreal.'.format(
            cantidad, que_en, donde_en, MARCA)
    else:
        descripcion_fr = 'Propriétés à vendre {}. Photos, prix et visites avec {}, courtiers immobiliers à Montréal.'.format(
            donde_fr, MARCA)
        descripcion_en = 'Properties for sale {}. Photos, prices and viewings with {}, real estate brokers in Montreal.'.format(
            donde_en, MARCA)

    return SimpleNamespace(
        m_title_f='{} | {}'.format(encabezado_fr, MARCA),
        m_title_a='{} | {}'.format(encabezado_en, MARCA),
        m_description_f=descripcion_fr,
        m_description_a=descripcion_en,
        encabezado_f=encabezado_fr,
        encabezado_a=encabezado_en,
    )
