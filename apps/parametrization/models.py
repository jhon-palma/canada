from .data_load.models import *
from .choices import *
from .files_path import *
from datetime import datetime, timedelta
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    cellphone = models.CharField(max_length=15, blank=True, null=False)
    telephone = models.CharField(max_length=15, blank=True, null=False)
    photo = models.ImageField(default='companys/photos/no_photo.png', upload_to=company_path, blank=True, null=False)

    class Meta:
        db_table = 'company'
        verbose_name = 'company'
        verbose_name_plural = 'Crear Empresas'
        ordering = ['name']

    def __str__(self):
        return self.name


