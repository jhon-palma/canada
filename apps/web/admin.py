from django.contrib import admin
from related_admin import RelatedFieldAdmin
from related_admin import getter_for_related_field
from .models import Statistics



@admin.register(Statistics)
class StatisticsAdmin(RelatedFieldAdmin):
    list_display = ['name',]
    list_filter = ['name',]
    search_fields = ['name',]

   