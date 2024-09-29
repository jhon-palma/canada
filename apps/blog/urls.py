from django.urls import include, path, re_path
from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

urlpatterns = [
    re_path(r'^(?P<language>fr|en)/blog/$', articles, name='articles'),
    path('new-post', login_required(new_post), name='new_post'),
    path('new-category', login_required(new_category), name='new_category'),
    path('list_articles/', login_required(list_articles), name='list_articles'),
    re_path('list_comment_article/(?P<article_id>[\w-]+)/$', login_required(list_comment_article), name='list_comment_article'),
    re_path('update_article/(?P<article_id>[\w-]+)/$',login_required(update_article), name='update_article'),
    path('category/update/<uuid:uuid>/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/', categories, name='categories'),
    re_path(r'^(?P<language>fr|en)/blog/(?P<slug>[-\w]+)/$', detail, name='post_detail'),
    path('update_status_ajax/', update_status_ajax, name='update_status_ajax'),
    re_path(r'^(?P<language>fr|en)/blog/article/like/(?P<category_slug>[-\w]+)/(?P<slug>[-\w]+)/$', like_article, name='like_article'),
    path('comment/', comment, name='comment'),
    path('signup/', signup_blog, name='signup_blog'),
    path('signupComment/', signup_blog_comment, name='signup_blog_comment'),
    path('login/', login_blog, name='login_blog'),
    path('loginComments/', login_blog_comments, name='login_blog_comments'),
    path('update_status_comment/', login_required(update_status_comment), name='update_status_comment'),
    path('<slug:slug>/', category, name='category_detail'),
]