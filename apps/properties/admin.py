#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from related_admin import RelatedFieldAdmin
from related_admin import getter_for_related_field
from .models import *

admin.site.register(Membres)

@admin.register(Inscriptions)
class InscriptionsAdmin(RelatedFieldAdmin):
    list_display = ['no_inscription','genre_propriete__description_anglaise','mun_code__description','nom_rue_complet','appartement','status']
    list_filter = ['status']
    search_fields = ['no_inscription','nom_rue_complet']

   

