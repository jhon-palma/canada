# from django.contrib import admin
# from related_admin import RelatedFieldAdmin
# from related_admin import getter_for_related_field
# from ..users.models import *
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile



admin.site.register(Profile)
