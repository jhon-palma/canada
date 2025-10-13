from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('profile_list/', profile_list, name='profile_list'),
    path('users_blog_list/', users_blog_list, name='users_blog_list'),
    path('profile/', update_profile, name='profile'),
    re_path('update_user_blog/(?P<user_id>[\w-]+)/$', update_user_blog, name='update_user_blog'),
    re_path('profile/update/(?P<user_id>[\w-]+)/$', update_profile_users, name='update_profile'),
    path('password_change/',login_required(change_password), name='password_change'),
    path('password_change/done/',password_change_done, name='password_change_done'),
    re_path('password_change_user/(?P<user_id>[\w-]+)/$', login_required(change_password_user), name='password_change_user'),
    path('create_user/',login_required(create_user), name='create_user'),
    path('list_messages/',login_required(list_messages), name='list_messages'),
    re_path('detail_message/(?P<id>[\w-]+)/$', login_required(detail_message), name='detail_message'),
    re_path('delete_message/(?P<id>[\w-]+)/$', login_required(delete_message), name='delete_message'),
    path('list_images/',login_required(list_images), name='list_images'),
    re_path('update_image/(?P<image_id>[\w-]+)/$',login_required(update_image), name='update_image'),
]