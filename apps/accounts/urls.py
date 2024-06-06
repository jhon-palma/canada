from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path

from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
]
