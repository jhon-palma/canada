from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.db.models.functions import Coalesce
from django.urls import reverse

from apps.blog.models import Article
from apps.properties.models import GenresProprietes, Inscriptions, Municipalites
from apps.seo import LANGUAGES, current_language, site_domain
from apps.users.models import Profile


class BaseSitemap(Sitemap):
    """Base para un sitio bilingue donde el idioma es un segmento de la URL
    (``/fr/...`` y ``/en/...``) y no un prefijo i18n de Django.

    ``i18n`` + ``alternates`` genera una entrada <url> por idioma con sus
    enlaces hreflang. Django activa el idioma antes de cada llamada a
    ``location()``, por eso se relee con ``language()``.
    """

    i18n = True
    alternates = True
    languages = LANGUAGES
    protocol = settings.SITE_PROTOCOL

    def get_domain(self, site=None):
        return site_domain()

    def language(self):
        return current_language()


# ---------------------------------------------------------------- paginas fijas

STATIC_ROUTES = {
    'index': {
        'url_name': 'web:index',
        'priority': 1.0,
        'changefreq': 'daily',
    },
    'properties': {
        'url_name': 'web:properties',
        'options': {'fr': 'proprietes', 'en': 'properties'},
        'priority': 0.9,
        'changefreq': 'daily',
    },
    'properties-for-sale': {
        'url_name': 'web:properties',
        'options': {'fr': 'proprietes-a-vendre', 'en': 'properties-for-sale'},
        'priority': 0.9,
        'changefreq': 'daily',
    },
    'properties-for-rent': {
        'url_name': 'web:properties',
        'options': {'fr': 'proprietes-a-louer', 'en': 'properties-for-rent'},
        'priority': 0.9,
        'changefreq': 'daily',
    },
    'team': {
        'url_name': 'web:team',
        'options': {'fr': 'courtier-immobilier', 'en': 'real-estate-broker'},
        'priority': 0.8,
        'changefreq': 'monthly',
    },
    'buying': {
        'url_name': 'web:work',
        'options': {'fr': 'acheter', 'en': 'buying'},
        'priority': 0.7,
        'changefreq': 'monthly',
    },
    'selling': {
        'url_name': 'web:work',
        'options': {'fr': 'vendre', 'en': 'selling'},
        'priority': 0.7,
        'changefreq': 'monthly',
    },
    'blog': {
        'url_name': 'blog:articles',
        'priority': 0.7,
        'changefreq': 'weekly',
    },
    'videos': {
        'url_name': 'web:videos',
        'priority': 0.6,
        'changefreq': 'weekly',
    },
    'contact': {
        'url_name': 'web:contact',
        'options': {'fr': 'contact-courtier-immobilier', 'en': 'contact-realestate-broker'},
        'priority': 0.6,
        'changefreq': 'yearly',
    },
    'privacy-policy': {
        'url_name': 'web:privacy-policy',
        'options': {'fr': 'politique-confidentialite', 'en': 'privacy-policy'},
        'priority': 0.2,
        'changefreq': 'yearly',
    },
}


class StaticViewSitemap(BaseSitemap):

    def items(self):
        return list(STATIC_ROUTES)

    def location(self, item):
        route = STATIC_ROUTES[item]
        kwargs = {'language': self.language()}
        options = route.get('options')
        if options:
            kwargs['option'] = options[self.language()]
        return reverse(route['url_name'], kwargs=kwargs)

    def priority(self, item):
        return STATIC_ROUTES[item]['priority']

    def changefreq(self, item):
        return STATIC_ROUTES[item]['changefreq']


# ------------------------------------------------------------------ inscriptions

class PropertieSitemap(BaseSitemap):
    """Fichas de propiedades activas: /<lang>/propriete|propertie/<uuid>/detail/."""

    priority = 0.8
    changefreq = 'weekly'
    limit = 20000
    options = {'fr': 'propriete', 'en': 'propertie'}

    def items(self):
        return Inscriptions.objects.filter(status=True).only('id', 'date_modif').order_by('id')

    def location(self, item):
        language = self.language()
        return reverse('web:detail-propertie', kwargs={
            'language': language,
            'option': self.options[language],
            'propertie_id': item.id,
            'flag': 'detail',
        })

    def lastmod(self, item):
        return item.date_modif

    def get_latest_lastmod(self):
        return Inscriptions.objects.filter(status=True).order_by('-date_modif') \
            .values_list('date_modif', flat=True).first()


# ------------------------------------------------- landings de busqueda (SEO)

class MunicipaliteSitemap(BaseSitemap):
    """/search/<lang>/<slug>/ por municipalidad (mismos enlaces que el footer)."""

    priority = 0.7
    changefreq = 'daily'
    slugs = {'fr': 'slug_francaise', 'en': 'slug_anglaise'}

    def items(self):
        return Municipalites.objects.filter(
            municipalite_code__isnull=False,
            slug_francaise__isnull=False,
            slug_anglaise__isnull=False,
        ).only('slug_francaise', 'slug_anglaise').order_by('code').distinct()

    def location(self, item):
        language = self.language()
        return reverse('web:search_properties', kwargs={
            'language': language,
            'option': getattr(item, self.slugs[language]),
        })


class GenreProprieteSitemap(MunicipaliteSitemap):
    """/search/<lang>/<slug>/ por categoria de propiedad."""

    def items(self):
        return GenresProprietes.objects.filter(
            genre_proprietes__isnull=False,
            slug_francaise__isnull=False,
            slug_anglaise__isnull=False,
        ).only('slug_francaise', 'slug_anglaise').order_by('genre_propriete').distinct()


# ----------------------------------------------------------------------- courtiers

class MemberSitemap(BaseSitemap):
    """/<lang>/courtier/<membre_uuid>/ para los corredores publicados en el equipo."""

    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return Profile.objects.filter(
            user__is_active=True,
            membre__isnull=False,
        ).exclude(order__isnull=True).order_by('order')

    def location(self, item):
        return reverse('web:member', kwargs={
            'language': self.language(),
            'option': 'courtier',
            'member_id': item.membre_id,
        })


# --------------------------------------------------------------------------- blog

class ArticleSitemap(BaseSitemap):
    """/<lang>/blog/<slug>/ para los articulos activos."""

    priority = 0.7
    changefreq = 'weekly'
    slugs = {'fr': 'slug_francaise', 'en': 'slug_anglaise'}

    def items(self):
        return Article.objects.filter(
            active=True,
            slug_francaise__isnull=False,
            slug_anglaise__isnull=False,
        )

    def location(self, item):
        language = self.language()
        return reverse('blog:post_detail', kwargs={
            'language': language,
            'slug': getattr(item, self.slugs[language]),
        })

    def lastmod(self, item):
        return item.date_hour or item.created_at

    def get_latest_lastmod(self):
        # Misma expresion que lastmod() para que el <lastmod> del indice no
        # quede por debajo del de sus propias entradas.
        return self.items().annotate(last=Coalesce('date_hour', 'created_at')) \
            .order_by('-last').values_list('last', flat=True).first()


SITEMAPS = {
    'static': StaticViewSitemap,
    'properties': PropertieSitemap,
    'municipalities': MunicipaliteSitemap,
    'categories': GenreProprieteSitemap,
    'members': MemberSitemap,
    'blog': ArticleSitemap,
}
