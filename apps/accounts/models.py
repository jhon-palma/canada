from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from apps.properties.models import Membres
from urllib.parse import quote
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return "/users/%s" % quote(self.email)
    
    def get_full_name(self) -> str:
        return super().get_full_name()
    