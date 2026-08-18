"""Helpers compartidos para URLs canonicas y idioma.

El sitio es bilingue con el idioma como segmento de la URL (``/fr/...`` y
``/en/...``), no con los prefijos i18n de Django, y no usa LocaleMiddleware.
Estas utilidades centralizan las dos cosas que de ahi se derivan: normalizar
el idioma activo y construir URLs absolutas sobre el dominio canonico.
"""

from django.conf import settings
from django.utils.translation import get_language

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
