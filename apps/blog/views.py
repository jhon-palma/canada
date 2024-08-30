from django.shortcuts import get_object_or_404, redirect, render
from .models import Article, Category
from .forms import ArticleForm, CategoryAdminForm, CommentForm, PostAdminForm
from django.db.models import Q
from django.views.generic import ListView
from django.conf import settings
from django.contrib import messages

def articles(request):
    articles = Article.objects.all()
    for article in articles:
        print('########################')
        print(article.get_absolute_url)
        print(article.was_published_recently.admin_order_field)
        print(article.was_published_recently.boolean)
        print(article.was_published_recently.short_description)
        print(article.category.slug_francaise)
        print(article.slug_francaise)
        print('########################')
    return render(request, 'blog/post_list.html',{'articles':articles})

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
    print('**********************')
    post = get_object_or_404(Article, slug_francaise=slug, status=Article.ACTIVE)


    return render(request, 'blog/detail.html', {'post': post})

def category(request, slug):
    category = get_object_or_404(Category, slug_francaise=slug)
    articles = category.posts.filter(status=Article.ACTIVE)

    return render(request, 'blog/post_list.html', {'category': category, 'articles': articles})