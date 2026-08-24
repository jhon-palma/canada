import pdb
from django.db import IntegrityError
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.accounts.models import CustomUser
from apps.users.models import Profile
from apps.web.models import MetaDataWeb
from .models import Article, Category, Like, Comment
from .forms import ArticleForm, ArticleUpdateForm, CategoryAdminForm
from django.db.models import F, Q
from django.views.generic import ListView
from django.conf import settings
from django.contrib import messages
from ..labels import DICT_LABELS
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone



def articles(request, language='fr'):
    articles_list  = Article.objects.publicados()
    paginator = Paginator(articles_list, 12)
    page_number = request.GET.get('page')
    data_meta = MetaDataWeb.for_origin('blog')
    try:
        articles = paginator.page(page_number)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    labels = DICT_LABELS.get(language, {}).get('web', {})
    context = {
        'language':language,
        'labels':labels,
        'articles':articles,
        'paginator':paginator,
        'data_meta':data_meta,
    }
    return render(request, 'blog/blog.html',context)



def new_post(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if request.POST.get('content_francaise') == '<p>&nbsp;</p>':
            form.add_error('content_francaise', 'Este campo no puede estar vacío.')
        if request.POST.get('content_anglaise') == '<p>&nbsp;</p>':
            form.add_error('content_anglaise', 'Este campo no puede estar vacío.')

        if not form.is_valid():
            print("Formulario no válido. Errores:", form.errors)
            for field, errors in form.errors.items():
                print(f"Errores en el campo {field}: {errors}")
        else:
            try:
                post = form.save(commit=False)
                post.authors = request.user
                post.save()
                messages.success(request, 'Post creado correctamente', 'succesful')
                return redirect('blog:list_articles')
            except IntegrityError as e:
                form.add_error(None, 'Error al guardar el post: ' + str(e))
                print("Formulario no válido. Errores:", form.errors)
    return render(request, 'blog/new_post.html',{'form':form})



def list_articles(request):
    articles = Article.objects.all()
    return render(request, 'blog/post_list.html',{'articles':articles})



def new_category(request):
    form = CategoryAdminForm()
    if request.method == 'POST':
        form = CategoryAdminForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, 'Categoria creada correctamente', 'succesful')
            return redirect('blog:categories')  
        else:
            messages.error(request, 'Error al crear la categoria')
    return render(request, 'blog/new_category.html',{'form':form})



def categories(request):
    categories = Category.objects.all()
    return render(request, 'blog/list_category.html',{'categories':categories})



def articulo_no_encontrado(request, language):
    """404 con salida, para un articulo que no existe o que aun no ha salido.

    Devolver 404 es lo correcto: la URL no lleva a ningun contenido. Redirigir
    al listado en su lugar es lo que Google llama soft 404 -- una redireccion
    a una pagina que no es la pedida -- y en vez de conservar la URL la deja
    en el limbo del indice; es el mismo patron que se quito de las fichas de
    propiedades.

    Lo que si hacia falta arreglar es el callejon sin salida: antes esto era
    el 404 pelado de Django. Ahora la pagina lleva al listado del blog y
    muestra los ultimos articulos, que es lo que la persona venia a leer.
    """
    return render(request, 'blog/no_encontrado.html', {
        'language': language,
        'labels': DICT_LABELS.get(language, {}).get('web', {}),
        'ultimos': Article.objects.publicados()[:4],
        'data_meta': MetaDataWeb.for_origin('blog'),
    }, status=404)


def detail(request, language, slug):
    labels = DICT_LABELS.get(language).get('web')
    slug_field = 'slug_anglaise' if language == 'en' else 'slug_francaise'

    # Sin try/except alrededor de todo. Habia un `except: return redirect('/')`
    # que se tragaba cualquier cosa: un articulo inexistente y un fallo de
    # plantilla acababan los dos en un 302 a la portada. Para Google eso es un
    # soft 404, y ahora ademas afectaria a cada articulo programado hasta su
    # fecha. Ahora responde el 404 que corresponde -- no un 410, porque un
    # articulo programado si va a existir -- y un error de verdad se ve en el
    # log en lugar de disfrazarse de redireccion.
    post = Article.objects.visibles_para(request.user).filter(**{slug_field: slug}).first()
    if post is None:
        return articulo_no_encontrado(request, language)

    # Un articulo con fecha futura que se esta viendo: solo llega aqui alguien
    # del equipo, porque para el resto visibles_para() no lo devuelve.
    vista_previa = bool(post.date_hour and post.date_hour > timezone.now())

    # Con update() en vez de save(): un save() aqui reescribia la fila
    # completa -- los dos campos de contenido del editor incluidos -- en
    # cada visita, y ahora ademas movería updated_at, de modo que el
    # <lastmod> del sitemap cambiaria cada vez que alguien abre el
    # articulo. update() tampoco pierde incrementos si entran dos
    # visitas a la vez, porque suma en la base y no en memoria.
    # Las revisiones previas no cuentan como visitas: el articulo todavia no
    # lo ha visto nadie de fuera.
    if not vista_previa:
        Article.objects.filter(pk=post.pk).update(visites=F('visites') + 1)
        post.visites += 1
 
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(user=request.user, post=post).exists()

    # Por date_hour, para que seguir la flecha lleve al articulo que de
    # verdad esta al lado en el listado.
    referencia = post.date_hour or post.created_at
    previous_post = Article.objects.publicados().filter(
        date_hour__lt=referencia
    ).order_by('-date_hour').first()

    next_post = Article.objects.publicados().filter(
        date_hour__gt=referencia
    ).order_by('date_hour').first()
    
    if request.method == 'POST':
        return redirect('post_detail', slug=slug)

    context = {
        'language':language,
        'labels':labels,
        'post': post,
        'user_liked': user_liked,
        'previous_post': previous_post,
        'next_post': next_post,
        'data_meta':post,
        'vista_previa': vista_previa,
    }

    respuesta = render(request, 'blog/detail.html', context)
    if vista_previa:
        # Por si alguien del equipo comparte el enlace de la revision. Google
        # no deberia poder llegar -- sin sesion de staff esto es un 404 --,
        # pero la cabecera lo deja dicho explicitamente.
        respuesta['X-Robots-Tag'] = 'noindex, nofollow'
    return respuesta

   
  

def category(request, language, slug):
    """Listado publico de articulos de una categoria, en fr o en.

    Mismo contrato de contexto que `articles` para poder reutilizar
    blog/blog.html (que incluye web/header_web.html y pagina con `articles`).
    """
    slug_field = 'slug_anglaise' if language == 'en' else 'slug_francaise'
    category = get_object_or_404(Category, **{slug_field: slug})

    articles_list = category.posts.publicados()
    paginator = Paginator(articles_list, 12)
    try:
        articles = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {
        'language': language,
        'labels': DICT_LABELS.get(language, {}).get('web', {}),
        'articles': articles,
        'paginator': paginator,
        'data_meta': MetaDataWeb.for_origin('blog'),
        'category': category,
    }
    return render(request, 'blog/blog.html', context)



def update_article(request, article_id):
    post = get_object_or_404(Article, id=article_id)
    form = ArticleUpdateForm(instance=post)

    if request.method == 'POST':
        form = ArticleUpdateForm(request.POST, request.FILES, instance=post)
        if request.POST.get('content_francaise') == '<p>&nbsp;</p>':
            form.add_error('content_francaise', 'Este campo no puede estar vacío.')
        if request.POST.get('content_anglaise') == '<p>&nbsp;</p>':
            form.add_error('content_anglaise', 'Este campo no puede estar vacío.')

        if not form.is_valid():
            print("Formulario no válido. Errores:", form.errors)
            for field, errors in form.errors.items():
                print(f"Errores en el campo {field}: {errors}")
        else:
            try:
                post = form.save(commit=False)
                post.authors = request.user
                post.save()
                messages.success(request, 'Post actualizado correctamente', 'success')
                return redirect('blog:list_articles')
            except IntegrityError as e:
                form.add_error(None, 'Error al guardar el post: ' + str(e))
                print("Formulario no válido. Errores:", form.errors)

    return render(request, 'blog/update_post.html', {'form': form})




from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryAdminForm
    template_name = 'blog/new_category.html'
    success_url = reverse_lazy('blog:categories')

    def get_object(self, queryset=None):
        uuid_value = self.kwargs.get('uuid')
        return get_object_or_404(Category, id=uuid_value)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Categoría actualizada correctamente', extra_tags='successful')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, form.errors)
        return response



def update_categorys(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryAdminForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria actualizada correctamente', 'succesful')
            return redirect('blog:categories')  
        else:
            messages.error(request, form.errors)
    return render(request, 'blog/new_category.html',{'category':category})





def update_status_ajax(request):
    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        try:
            article = Article.objects.get(id=record_id)
            if article.active:
                article.active = False
                status_message = 'desactivado'
            else:
                article.active = True
                status_message = 'activado'
            article.save()
            articles = Article.objects.all()
            articles_html = render_to_string('blog/articles_list.html', {'articles': articles})
            return JsonResponse({'success': True, 'message': f'Registro {status_message} con éxito.','articles_html': articles_html})
        except Article.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Registro no encontrado'})
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

def like_article(request, language, category_slug, slug):

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    if language == 'en':
        article = get_object_or_404(Article, slug_anglaise=slug, active=True)
    else:
        article = get_object_or_404(Article, slug_francaise=slug, active=True)
    liked = Like.objects.filter(user=request.user, post=article).exists()
    if liked:
        Like.objects.filter(user=request.user, post=article).delete()
        liked = False
    else:
        Like.objects.create(user=request.user, post=article)
        liked = True

    likes_count = article.like_set.count()

    return JsonResponse({
        'liked': liked,
        'likes_count': likes_count
    })

def signup_blog(request):
    if request.method == 'POST':
        email = request.POST.get('email_signup')
        re_email = request.POST.get('re_mail_signup')
        password = request.POST.get('password_signup')
        re_password = request.POST.get('re_password_signup')
        language = request.POST.get('language')
        slug = request.POST.get('post_slug')

        if email != re_email:
            return JsonResponse({'success': False, 'error_message': 'Los correos electrónicos no coinciden.'})
        
        if password != re_password:
            return JsonResponse({'success': False, 'error_message': 'Las contraseñas no coinciden.'})

        try:
            # userBlog=True: sin esto el registro publico creaba cuentas
            # indistinguibles de las del equipo, y son las que decide
            # interno_required. signup_blog_comment ya lo hacia.
            user = CustomUser.objects.create_user(username=email, email=email, password=password, userBlog=True)
            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                if language == 'en':
                    article = get_object_or_404(Article, slug_anglaise=slug, active=True)
                else:
                    article = get_object_or_404(Article, slug_francaise=slug, active=True)
                liked = Like.objects.filter(user=user, post=article).exists()
                if not liked:
                    Like.objects.create(user=user, post=article)
                    liked = True

                likes_count = article.like_set.count()
                return JsonResponse({
                    'success': True,
                    'liked': liked,
                    'likes_count': likes_count
                })
        except IntegrityError:
            if language == "en":
                message = 'A user with this email already exists.'
            else:
                message = 'Un utilisateur avec cet email existe déjà.'
            return JsonResponse({'success': False, 'error_message': message})
        except ValidationError as e:
            return JsonResponse({'success': False, 'error_message': str(e)})

    return JsonResponse({'success': False, 'error_message': 'Método de solicitud no permitido.'})



def login_blog(request):
    if request.method == 'POST':
        email = request.POST.get('email_login')
        password = request.POST.get('password_login')
        language = request.POST.get('language')
        slug = request.POST.get('post_slug')
        try:
            validate_email(email)
        except ValidationError:
            if language == 'en': 
                message = 'Invalid email address'
            else:
                message = 'Courriel non valide'
            return JsonResponse({'success': False, 'error_message': message})
        try:
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                if language == 'en':
                        article = get_object_or_404(Article, slug_anglaise=slug, active=True)
                else:
                    article = get_object_or_404(Article, slug_francaise=slug, active=True)
                liked = Like.objects.filter(user=user, post=article).exists()
                if not liked:
                    Like.objects.create(user=user, post=article)
                    liked = True

                likes_count = article.like_set.count()
                return JsonResponse({
                        'success': True,
                        'liked': liked,
                        'likes_count': likes_count
                    })
            else:
                message = 'Invalid email or password'
                return JsonResponse({'success': False, 'error_message': message})
        except IntegrityError:
            if language == "en":
                message = 'A error exists.'
            else:
                message = 'Un error existe déjà.'
            return JsonResponse({'success': False, 'error_message': message})
        except ValidationError as e:
            return JsonResponse({'success': False, 'error_message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})



def comment(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        slug = request.POST.get('post_slug')
        comment_user = request.POST.get('comment')
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        if language == 'en':
            article = get_object_or_404(Article, slug_anglaise=slug, active=True)
        else:
            article = get_object_or_404(Article, slug_francaise=slug, active=True)
        comment = Comment()
        comment.article = article
        comment.comment = comment_user
        comment.user = request.user
        comment.save()
        
        return JsonResponse({
            'success': True,
        })



def signup_blog_comment(request):
    if request.method == 'POST':
        email = request.POST.get('email_signup')
        re_email = request.POST.get('re_mail_signup')
        password = request.POST.get('password_signup')
        re_password = request.POST.get('re_password_signup')
        language = request.POST.get('language')
        slug = request.POST.get('post_slug')
        comment_user = request.POST.get('comment')

        if email != re_email:
            return JsonResponse({'success': False, 'error_message': 'Los correos electrónicos no coinciden.'})
        
        if password != re_password:
            return JsonResponse({'success': False, 'error_message': 'Las contraseñas no coinciden.'})

        try:
            # user = CustomUser.objects.create_user(username=email, email=email, password=password)
            user = CustomUser.objects.create_user(username=email, email=email, password=password, userBlog=True)
            if user:
                Profile.objects.create(user=user) 
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                if language == 'en':
                    article = get_object_or_404(Article, slug_anglaise=slug, active=True)
                else:
                    article = get_object_or_404(Article, slug_francaise=slug, active=True)
                comment = Comment()
                comment.article = article
                comment.comment = comment_user
                comment.user = user
                comment.save()

                return JsonResponse({
                    'success': True,
                })
        except IntegrityError:
            if language == "en":
                message = 'A user with this email already exists.'
            else:
                message = 'Un utilisateur avec cet email existe déjà.'
            return JsonResponse({'success': False, 'error_message': message})
        except ValidationError as e:
            return JsonResponse({'success': False, 'error_message': str(e)})

    return JsonResponse({'success': False, 'error_message': 'Método de solicitud no permitido.'})



def login_blog_comments(request):
    if request.method == 'POST':
        email = request.POST.get('email_login')
        password = request.POST.get('password_login')
        language = request.POST.get('language')
        slug = request.POST.get('post_slug')
        comment_user = request.POST.get('comment')
        try:
            validate_email(email)
        except ValidationError:
            if language == 'en': 
                message = 'Invalid email address'
            else:
                message = 'Courriel non valide'
            return JsonResponse({'success': False, 'error_message': message})

        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if language == 'en':
                article = get_object_or_404(Article, slug_anglaise=slug, active=True)
            else:
                article = get_object_or_404(Article, slug_francaise=slug, active=True)
            comment = Comment()
            comment.article = article
            comment.comment = comment_user
            comment.user = user
            comment.save()

            return JsonResponse({
                'success': True,
            })
        else:
            message = 'Invalid email or password'
            return JsonResponse({'success': False, 'error_message': message})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def list_comment_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = article.comments.all()
    return render(request, 'blog/list_comment_article.html',{'article':article, 'comments': comments,})

def update_status_comment(request):
    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        try:
            comment = Comment.objects.get(id=record_id)
            if comment.active:
                comment.active = False
                status_message = 'desactivado'
            else:
                comment.active = True
                status_message = 'activado'
            comment.save()
            article = comment.article
            comments = article.comments.all()
            comments_html = render_to_string('blog/comments_list.html', {'comments': comments})
            return JsonResponse({'success': True, 'message': f'Registro {status_message} con éxito.','comments_html': comments_html})
        except Article.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Registro no encontrado'})
    return JsonResponse({'success': False, 'message': 'Método no permitido'})