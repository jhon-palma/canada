import uuid
from django.db import models
from apps.web.files_path import web_images_path
from apps.web.choices import *
from PIL import Image


class Formulaire_contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    no_formulaire = models.IntegerField()  
    nom = models.CharField(max_length=100, blank=True, null=True)
    courriel = models.EmailField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    adresse = models.CharField(max_length=255,blank=True, null=True)
    sujet = models.CharField(max_length=100)
    read = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_lecture = models.DateTimeField(null=True, blank=True)
    tag = models.CharField(max_length=50, blank=True, null=True)
    broker = models.CharField(max_length=100, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.no_formulaire:
            last_instance = Formulaire_contact.objects.order_by('-no_formulaire').first()
            if last_instance:
                self.no_formulaire = last_instance.no_formulaire + 1
            else:
                self.no_formulaire = 1
        super(Formulaire_contact, self).save(*args, **kwargs)


class Statistics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(choices=WEB_STATICTS_CHOICES, max_length=20, null=False, blank=False)
    initial_year = models.CharField(max_length=4, blank=True, null=True)
    final_year = models.CharField(max_length=4, blank=True, null=True)
    initial_value = models.CharField(max_length=50, blank=True, null=True)
    final_value = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'web_statistics'
        verbose_name = 'web_statistics'


class ImagesWeb(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    reference = models.CharField(choices=WEB_IMAGES_CHOICES, max_length=30, null=False, blank=False)
    image = models.ImageField(upload_to=web_images_path, null=False, blank=False)
    order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'web_images'
        verbose_name = 'web_images'
    
    def __str__(self):
        return self.reference
    
    @property
    def get_info(self):
        with Image.open(self.image) as img:
            data = {
                'format':img.format,
                'size':img.size
            }
        return data
    


class VideosWeb(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    tittle = models.CharField(max_length=120)
    description = models.TextField()
    videoId = models.CharField(max_length=100)
    publishedAt = models.DateTimeField()
    is_short = models.BooleanField(default=False)
    
    def __str__(self):
        return self.tittle
    


class MetaDataWeb(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    origin = models.CharField(choices=WEB_META_ORIGIN_CHOICES, max_length=10, null=False, default='index')
    m_title_a = models.TextField(blank=False, null=True)
    m_title_f = models.TextField(blank=False, null=True)
    m_description_a = models.TextField(blank=False, null=True)
    m_description_f = models.TextField(blank=False, null=True)
    
    class Meta:
        db_table = 'web_metadata'
        verbose_name = 'web_metadata'
    
    def __str__(self):
        return self.origin
    
    