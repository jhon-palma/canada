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
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES) 
        if form.is_valid:
            post = form.save(commit=False)
            post.authors = request.user
            post.save()
            messages.success(request, 'Post creado correctamente', 'succesful')
            return redirect('blog:articles')
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

def detail(request, category_slug, slug):
    language = request.GET.get('language', 'fr')
    labels = DICT_LABELS.get(language).get('web')
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
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES)
            #if 'image' in request.FILES:  
            #    image_form.image = request.FILES['image'] 
            form.save()
            messages.success(request, 'Imagen Actualizada', 'succesful')
            return redirect('users:list_images') 

    return render(request, 'users/update_image.html',{'article':article})

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
