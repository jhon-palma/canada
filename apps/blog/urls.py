"""URLs del blog.

Las vistas de gestion exigen interno_required y no login_required. El blog
tiene registro publico -- signup_blog crea un CustomUser y lo deja con la
sesion iniciada -- asi que cualquiera que se registrase para comentar quedaba
autenticado y podia entrar a /list_articles/, crear articulos y editarlos.
update_status_ajax, que activa y desactiva articulos, no pedia siquiera eso.

La llave es userBlog=False, o sea cuenta del equipo, y no is_staff: publicar
no deberia exigir acceso al admin de Django.
"""

from django.urls import include, path, re_path
from apps.decorators import interno_required
from django.urls import path
from .views import *
from .ckeditor import upload_file as ckeditor_upload

urlpatterns = [
    re_path(r'^(?P<language>fr|en)/blog/$', articles, name='articles'),
    re_path(r'^(?P<language>fr|en)/blog/category/(?P<slug>[-\w]+)/$', category, name='category_detail'),
    path('new-post', interno_required(new_post), name='new_post'),
    path('new-category', interno_required(new_category), name='new_category'),
    path('list_articles/', interno_required(list_articles), name='list_articles'),
    re_path('list_comment_article/(?P<article_id>[\w-]+)/$', interno_required(list_comment_article), name='list_comment_article'),
    re_path('update_article/(?P<article_id>[\w-]+)/$',interno_required(update_article), name='update_article'),
    path('category/update/<uuid:uuid>/', interno_required(CategoryUpdateView.as_view()), name='category_update'),
    path('categories/', interno_required(categories), name='categories'),
    re_path(r'^(?P<language>fr|en)/blog/(?P<slug>[-\w]+)/$', detail, name='post_detail'),
    path('update_status_ajax/', interno_required(update_status_ajax), name='update_status_ajax'),
    re_path(r'^(?P<language>fr|en)/blog/article/like/(?P<category_slug>[-\w]+)/(?P<slug>[-\w]+)/$', like_article, name='like_article'),
    path('comment/', comment, name='comment'),
    path('signup/', signup_blog, name='signup_blog'),
    path('signupComment/', signup_blog_comment, name='signup_blog_comment'),
    path('login/', login_blog, name='login_blog'),
    path('loginComments/', login_blog_comments, name='login_blog_comments'),
    path('update_status_comment/', interno_required(update_status_comment), name='update_status_comment'),
    # La subida del editor, con el permiso del equipo en vez del is_staff
    # que exige la vista del paquete. Ver CK_EDITOR_5_UPLOAD_FILE_VIEW_NAME.
    path('ckeditor5/subir-imagen/', ckeditor_upload, name='ckeditor_upload'),
]
