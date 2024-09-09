import pdb
from django.db import IntegrityError
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.accounts.models import CustomUser
from .models import Article, Category, Like
from .forms import ArticleForm, CategoryAdminForm
from django.db.models import Q
from django.views.generic import ListView
from django.conf import settings
from django.contrib import messages
from ..labels import DICT_LABELS
from django.utils.translation import gettext as _
from babel.dates import format_date
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def articles(request, language='fr'):
    articles_list  = Article.objects.filter(active=True)
    paginator = Paginator(articles_list, 12)
    page_number = request.GET.get('page')
    try:
        articles = paginator.page(page_number)
    except PageNotAnInteger:
        # Si el número de página no es un entero, muestra la primera página
        articles = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango, muestra la última página de resultados
        articles = paginator.page(paginator.num_pages)
    labels = DICT_LABELS.get(language, {}).get('web', {})
    # labels = DICT_LABELS.get(language).get('web')
    for article in articles:
        article.formatted_date = format_date(article.created_at, format='d MMMM yyyy', locale=language)

    context = {
        'language':language,
        'labels':labels,
        'articles': articles,
        'paginator': paginator,
    }
    return render(request, 'blog/blog.html',context)

def new_post(request):
    form = ArticleForm()
    language = request.GET.get('language', 'fr')
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
    # language = request.GET.get('language', 'fr')
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

def detail(request, language, category_slug, slug):
    labels = DICT_LABELS.get(language).get('web')
    if language == 'en':
        post = get_object_or_404(Article, slug_anglaise=slug, active=True)
    else:
        post = get_object_or_404(Article, slug_francaise=slug, active=True)
    post.visites += 1
    post.save()

    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(user=request.user, post=post).exists()

    previous_post = Article.objects.filter(
        active=True,
        created_at__lt=post.created_at
    ).order_by('-created_at').first()
    
    next_post = Article.objects.filter(
        active=True,
        created_at__gt=post.created_at
    ).order_by('created_at').first()
    
    if request.method == 'POST':
        

            return redirect('post_detail', slug=slug)

    context = {
        'language':language,
        'labels':labels,
        
        'post': post,
        'user_liked': user_liked,
        'previous_post': previous_post,
        'next_post': next_post,
    }

    return render(request, 'blog/detail.html', context)

def category(request, slug):
    category = get_object_or_404(Category, slug_francaise=slug)
    articles = category.posts.filter(status=Article.ACTIVE)

    return render(request, 'blog/post_list.html', {'category': category, 'articles': articles})

def update_article(request, article_id):
    post = get_object_or_404(Article, id=article_id)
    form = ArticleForm(instance=post)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=post)
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

    return render(request, 'blog/new_post.html', {'form': form})

def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryAdminForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, 'Categoria actualizada correctamente', 'succesful')
            return redirect('blog:categories')  
        else:
            messages.error(request, 'Error al actualizar la categoria')
    return render(request, 'blog/new_category.html',{'category':category})

@csrf_exempt
def update_status_ajax(request):
    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        try:
            article = Article.objects.get(id=record_id)
            if article.active:
                article.active = False
                status_message = 'activado'
            else:
                article.active = True
                status_message = 'inactivado'
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
            user = CustomUser.objects.create_user(username=email, email=email, password=password)
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
        print(email)
        try:
            # Validate email format
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

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def comment(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        slug = request.POST.get('post_slug')

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
