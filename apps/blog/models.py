from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import datetime
from django.utils.text import slugify
from django.utils.translation import get_language
from googletrans import Translator
import uuid
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.sites.models import Site
from apps.accounts.models import CustomUser

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title_anglaise = models.CharField(max_length=255)
    title_francaise = models.CharField(max_length=255)
    slug_francaise = models.SlugField()
    slug_anglaise = models.SlugField()

    class Meta:
        ordering = ('title_francaise',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        language = get_language()  # Obtiene el idioma actual
        if language == 'fr':
            return self.title_francaise
        elif language == 'en': 
            return self.title_anglaise
        else:
            return self.title_francaise

    def get_absolute_url(self):
        language = get_language()  # Obtiene el idioma actual
        if language == 'fr':  # Ejemplo: idioma francés
            return '/%s/' % self.slug_francaise
        elif language == 'en':  # Ejemplo: idioma inglés
            return '/%s/' % self.slug_anglaise
        else:
            return '/%s/' % self.slug_francaise

    def save(self, *args, **kwargs):
        self.slug_francaise = slugify(self.title_anglaise)
        self.slug_anglaise = slugify(self.title_anglaise)

        super(Category, self).save(*args, **kwargs)

class Article(models.Model):
    ACTIVE = 'active'
    DRAFT = 'draft'

    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (DRAFT, 'Draft')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE, blank=False, null=False)
    title_francaise = models.CharField(max_length=255)
    title_anglaise = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=ACTIVE)
    image_francaise = models.ImageField(default='blog/images/default.png', upload_to='blog/images/', blank=True, null=True)
    image_anglaise = models.ImageField(default='blog/images/default.png', upload_to='blog/images/', blank=True, null=True)
    content_francaise = CKEditor5Field('ContentFrancaise', config_name='extends', blank=False, null=False)
    content_anglaise = CKEditor5Field('ContentAnglaise', config_name='extends', blank=False, null=False)
    authors = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug_francaise = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    slug_anglaise = models.SlugField(max_length=150, unique=True, blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        language = get_language()
        if language == 'fr':
            relative_url = '/blog/%s/%s/' % (self.category.slug_francaise, self.slug_francaise)
        elif language == 'en':  # Ejemplo: idioma inglés
            relative_url = '/blog/%s/%s/' % (self.category.slug_anglaise, self.slug_anglaise)
        else:
            relative_url = '/blog/%s/%s/' % (self.category.slug_francaise, self.slug_francaise)
        
        # Obtiene el dominio actual del sitio
        current_site = Site.objects.get_current()
        domain = current_site.domain

        scheme = 'https' if settings.USE_HTTPS else 'http'
        return f'{scheme}://{domain}{relative_url}'
    
    def was_published_recently(self):
        """Checks if the post was published recently.

        Returns:
            bool: True if the post was published recently, False otherwise.
        """
        return self.created_at >= timezone.now().date() - datetime.timedelta(days=7)

    was_published_recently.admin_order_field = "created_at"
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently?"

    def save(self, *args, **kwargs):
       

        self.slug_francaise = slugify(self.title_francaise)
        self.slug_anglaise = slugify(self.title_anglaise)

        super(Article, self).save(*args, **kwargs)

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Like(models.Model):
    post = models.ForeignKey(Article, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)