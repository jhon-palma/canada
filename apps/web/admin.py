from django.contrib import admin
from related_admin import RelatedFieldAdmin
from related_admin import getter_for_related_field
from .models import *



admin.site.register(Statistics)
admin.site.register(ImagesWeb)
admin.site.register(MetaDataWeb)
