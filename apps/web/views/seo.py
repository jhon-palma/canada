from django.contrib.sitemaps.views import SitemapIndexItem, x_robots_tag
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import TemplateView

from apps.seo import site_domain, site_url


@x_robots_tag
def sitemap_index(request, sitemaps, template_name='sitemap_index.xml',
                  content_type='application/xml'):
    """Equivalente a django.contrib.sitemaps.views.index, pero usando el
    dominio canonico de settings en vez del registro de la tabla django_site
    (que sigue en example.com)."""
    domain = site_domain()
    sections = []
    for section, sitemap_class in sitemaps.items():
        sitemap = sitemap_class() if callable(sitemap_class) else sitemap_class
        protocol = sitemap.protocol or request.scheme
        location = '{}://{}{}'.format(
            protocol,
            domain,
            reverse('django.contrib.sitemaps.views.sitemap', kwargs={'section': section}),
        )
        last_mod = sitemap.get_latest_lastmod()
        sections.append(SitemapIndexItem(location, last_mod))
        for page in range(2, sitemap.paginator.num_pages + 1):
            sections.append(SitemapIndexItem('{}?p={}'.format(location, page), last_mod))

    return TemplateResponse(
        request, template_name, {'sitemaps': sections}, content_type=content_type
    )


class RobotsTxtView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_url'] = site_url()
        return context
