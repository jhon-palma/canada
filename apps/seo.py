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
