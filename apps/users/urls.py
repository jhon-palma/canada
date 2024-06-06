from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import change_password, create_user, detail_message, list_messages, password_change_done, profile_list, updateProfile, updateProfileUsers, change_password_user

urlpatterns = [
    path('profileList/', profile_list, name='profile_list'),
    path('profile/', updateProfile, name='profile'),
    re_path('profile/update/(?P<user_id>[\w-]+)/$', updateProfileUsers, name='update_profile'),
    path('password_change/',login_required(change_password), name='password_change'),
    path('password_change/done/',password_change_done, name='password_change_done'),
    re_path('password_change_user/(?P<user_id>[\w-]+)/$', login_required(change_password_user), name='password_change_user'),
    path('create_user/',login_required(create_user), name='create_user'),
    path('list_messages/',login_required(list_messages), name='list_messages'),
    re_path('detail_message/(?P<id>[\w-]+)/$', login_required(detail_message), name='detail_message'),
]