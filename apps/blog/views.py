import pdb
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from .models import Article, Category
from .forms import ArticleForm, CategoryAdminForm, CommentForm
from django.db.models import Q
from django.views.generic import ListView
from django.conf import settings
from django.contrib import messages
from ..labels import DICT_LABELS
from django.utils.translation import gettext as _
from babel.dates import format_date

def articles(request, language='fr'):
    articles = Article.objects.all()
    labels = DICT_LABELS.get(language, {}).get('web', {})
    labels = DICT_LABELS.get(language).get('web')
    # for article in articles:
    #     print('########################')
    #     print(language)
    #     print(article.get_absolute_url)
    #     print(article.was_published_recently.admin_order_field)
    #     print(article.was_published_recently.boolean)
    #     print(article.was_published_recently.short_description)
    #     print(article.category.slug_francaise)
    #     print(article.slug_francaise)
    #     print('########################')
    for article in articles:
        article.formatted_date = format_date(article.created_at, format='d MMMM yyyy', locale=language)

    context = {
        'language':language,
        'labels':labels,
        'articles': articles,
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
        post = get_object_or_404(Article, slug_anglaise=slug, status=Article.ACTIVE)
    else:
        post = get_object_or_404(Article, slug_francaise=slug, status=Article.ACTIVE)
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()
    context = {
        'language':language,
        'labels':labels,
        'form': form,
        'post': post,
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
