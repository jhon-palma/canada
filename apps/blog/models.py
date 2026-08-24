from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.utils.text import slugify
from googletrans import Translator
import uuid
from django_ckeditor_5.fields import CKEditor5Field
from apps.accounts.models import CustomUser
from apps.decorators import is_internal_user
from apps.seo import absolute_url, current_language, normalize_language



class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title_anglaise = models.CharField(max_length=255)
    title_francaise = models.CharField(max_length=255)
    slug_francaise = models.SlugField(unique=True,)
    slug_anglaise = models.SlugField(unique=True,)

    class Meta:
        ordering = ('title_francaise',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        title = '{} | {}'.format(self.title_francaise, self.title_anglaise)
        return title

    def get_absolute_url(self, language=None):
        language = normalize_language(language) if language else current_language()
        slug = self.slug_anglaise if language == 'en' else self.slug_francaise
        return reverse('blog:category_detail', kwargs={'language': language, 'slug': slug})

    def save(self, *args, **kwargs):
        self.slug_francaise = slugify(self.title_francaise)
        self.slug_anglaise = slugify(self.title_anglaise)
        super(Category, self).save(*args, **kwargs)



class ArticleQuerySet(models.QuerySet):

    def publicados(self):
        """Los articulos que un visitante puede ver.

        Activos y con la fecha de publicacion ya cumplida. Antes bastaba con
        active=True y date_hour no filtraba nada, asi que poner una fecha
        futura en el formulario publicaba el articulo al instante igualmente.

        Los que tengan date_hour a nulo cuentan como publicados: el campo
        admite nulos y no hay motivo para esconder un articulo por no tener
        fecha.
        """
        return self.filter(active=True).filter(
            models.Q(date_hour__isnull=True) | models.Q(date_hour__lte=timezone.now()))

    def visibles_para(self, user):
        """Lo mismo, mas los programados si quien mira es del equipo.

        Del equipo es cualquier cuenta con userBlog=False, el mismo criterio
        que abre las vistas de gestion: quien puede escribir un articulo puede
        verlo. Cubre los dos motivos por los que un articulo no es publico --
        que aun no le toque por fecha y que este retirado --, porque en ambos
        hace falta poder mirar como queda antes de sacarlo. Solo aplica al entrar por su URL: los listados, las
        categorias y el sitemap siguen usando publicados(), para que el equipo
        vea el sitio tal cual lo ve el visitante y el articulo no se escape a
        Google antes de tiempo.
        """
        if is_internal_user(user):
            return self.all()
        return self.publicados()


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE, blank=False, null=False)
    title_francaise = models.CharField(max_length=255)
    title_anglaise = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    date_hour = models.DateTimeField(default=timezone.now, null=True, blank=True)
    # created_at es auto_now_add: no se mueve al editar, asi que no servia
    # para el <lastmod> del sitemap. Y date_hour es la fecha de publicacion,
    # que es otra cosa. Este si registra la ultima modificacion real.
    updated_at = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(default=True)
    image_francaise = models.ImageField(default='public/web/blog/images/default.png', upload_to='public/web/blog/images/', blank=True, null=True)
    image_anglaise = models.ImageField(default='public/web/blog/images/default.png', upload_to='public/web/blog/images/', blank=True, null=True)
    content_francaise = CKEditor5Field('ContentFrancaise', config_name='extends', blank=False, null=False)
    content_anglaise = CKEditor5Field('ContentAnglaise', config_name='extends', blank=False, null=False)
    authors = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug_francaise = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    slug_anglaise = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    visites = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(CustomUser, related_name='likes', through='Like')
    m_title_a = models.CharField(max_length=100, blank=True, null=True)
    m_title_f = models.CharField(max_length=100, blank=True, null=True)
    m_description_a = models.CharField(max_length=100, blank=True, null=True)
    m_description_f = models.CharField(max_length=100, blank=True, null=True)

    objects = ArticleQuerySet.as_manager()

    class Meta:
        # Por fecha de publicacion, que es la que el redactor controla.
        # created_at queda de desempate para los que no tengan date_hour.
        ordering = ('-date_hour', '-created_at')

    @property
    def esta_publicado(self):
        """Si un visitante cualquiera puede verlo ahora mismo.

        Mismo criterio que ArticleQuerySet.publicados(), en una sola ficha.
        """
        return self.active and (self.date_hour is None or self.date_hour <= timezone.now())

    @property
    def estado(self):
        """'publicado', 'programado' o 'retirado'.

        active y date_hour son dos interruptores distintos: active es
        "retirado a mano" y date_hour es "todavia no le toca". active manda,
        asi que un articulo desactivado sigue retirado aunque le llegue su
        fecha. Esto los resume en una palabra para el listado de gestion, que
        antes no mostraba ni la fecha ni el estado y obligaba a deducirlo del
        icono del boton.
        """
        if not self.active:
            return 'retirado'
        if self.date_hour and self.date_hour > timezone.now():
            return 'programado'
        return 'publicado'

    def get_absolute_url(self, language=None):
        """URL absoluta del articulo: <SITE_URL>/<lang>/blog/<slug>/.

        Se usa en los botones de compartir de blog/detail.html, por eso es
        absoluta. Sin argumento toma el idioma activo normalizado.
        """
        language = normalize_language(language) if language else current_language()
        slug = self.slug_anglaise if language == 'en' else self.slug_francaise
        relative_url = reverse('blog:post_detail', kwargs={'language': language, 'slug': slug})
        return absolute_url(relative_url)

    def was_published_recently(self):
        """Checks if the post was published recently.

        Returns:
            bool: True if the post was published recently, False otherwise.
        """
        return self.created_at >= timezone.now().date() - datetime.timedelta(days=7)

    was_published_recently.admin_order_field = "created_at"
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently?"

    def clean(self):
        if not self.slug_francaise and self.title_francaise:
            self.slug_francaise = slugify(self.title_francaise)
        if not self.slug_anglaise and self.title_anglaise:
            self.slug_anglaise = slugify(self.title_anglaise)

        super(Article, self).clean()

    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)



class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name



class Like(models.Model):
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')