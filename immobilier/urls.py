from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin', admin.site.urls),
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
    # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)