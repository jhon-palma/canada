from django.urls import include, path, re_path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    re_path(r'^(?P<language>fr|en)/blog/$', views.articles, name='articles'),
    path('new-post', views.new_post, name='new_post'),
    path('new-category', views.new_category, name='new_category'),
    path('list_articles/', views.list_articles, name='list_articles'),
    re_path('update_article/(?P<article_id>[\w-]+)/$',login_required(views.update_article), name='update_article'),
    re_path('update_category/(?P<category_id>[\w-]+)/$',login_required(views.update_category), name='update_category'),
    path('categories', views.categories, name='categories'),
    # re_path(r'^(?P<language>fr|en)/<slug:category_slug>/<slug:slug>/', views.detail, name='post_detail'),
    re_path(r'^(?P<language>fr|en)/blog/(?P<category_slug>[-\w]+)/(?P<slug>[-\w]+)/$', views.detail, name='post_detail'),
    path('update_status_ajax/', views.update_status_ajax, name='update_status_ajax'),
    re_path(r'^(?P<language>fr|en)/blog/article/like/(?P<category_slug>[-\w]+)/(?P<slug>[-\w]+)/$', views.like_article, name='like_article'),
    path('comment/', views.comment, name='comment'),
    path('signup/', views.signup_blog, name='signup_blog'),
    path('signupComment/', views.signup_blog_comment, name='signup_blog_comment'),
    path('login/', views.login_blog, name='login_blog'),
    path('loginComments/', views.login_blog_comments, name='login_blog_comments'),
    path('<slug:slug>/', views.category, name='category_detail'),
]