from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, register_converter
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from apps.web.sitemaps import SITEMAPS
from apps.web.views.seo import RobotsTxtView, sitemap_index

class UUIDConverter:
    regex = '[a-fA-F0-9\-]{36}'

    def to_python(self, value):
        import uuid
        return uuid.UUID(value)

    def to_url(self, value):
        return str(value)

register_converter(UUIDConverter, 'uuid')


urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin', admin.site.urls),
    path('robots.txt', RobotsTxtView.as_view(), name='robots-txt'),
    path('sitemap.xml', sitemap_index, {'sitemaps': SITEMAPS}, name='sitemap-index'),
    path('sitemap-<section>.xml', sitemap, {'sitemaps': SITEMAPS},
         name='django.contrib.sitemaps.views.sitemap'),
    path('', include(('apps.accounts.urls','accounts'), namespace='accounts')),
    path('', include(('apps.users.urls','users'), namespace='users')),
    path('', include(('apps.web.urls','web'), namespace='web')),
    path('', include(('apps.blog.urls','blog'), namespace='blog')),
    path('properties/', include(('apps.properties.urls','properties'), namespace='properties')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)