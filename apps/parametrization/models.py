from .choices import *
from .files_path import *
from datetime import datetime, timedelta
from django.db import models
import uuid



class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    cellphone = models.CharField(max_length=15, blank=True, null=False)
    telephone = models.CharField(max_length=15, blank=True, null=False)
    
    class Meta:
        db_table = 'admin_company'
        verbose_name = 'admin_company'
        verbose_name_plural = 'Crear Empresas'
        ordering = ['name']

    def __str__(self):
        return self.name



class TypeUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    english = models.CharField(max_length=60, blank=False, null=False)
    french = models.CharField(max_length=60, blank=False, null=False)

    class Meta:
        db_table = 'admin_type_user'
        verbose_name = 'admin_type_user'

    def __str__(self):
        return '{} | {}'.format(self.french, self.english)


