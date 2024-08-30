from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.articles, name='articles'),
    path('new-post', views.new_post, name='new_post'),
    path('new-category', views.new_category, name='new_category'),
    path('categories', views.categories, name='categories'),
    path('<slug:category_slug>/<slug:slug>/', views.detail, name='post_detail'),
    path('<slug:slug>/', views.category, name='category_detail'),
]