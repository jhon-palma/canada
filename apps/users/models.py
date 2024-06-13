from django.db import models
from django.db.models.signals import post_save
from PIL import Image

from apps.accounts.models import CustomUser
from apps.properties.models import Membres
from apps.users.choices import TYPE_USER



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='static/media/default.png', upload_to='static/media/profile_imgs')
    image_over = models.ImageField(default='static/media/default_over.png', upload_to='static/media/profile_imgs')
    order = models.SmallIntegerField(blank=True, null=True)
    membre = models.ForeignKey(Membres, on_delete=models.CASCADE, blank=True, null=True)
    type_user = models.CharField(default='admin', max_length=20, choices=TYPE_USER, blank=True, null=False)
    occupation = models.CharField(blank=True, max_length=60, null=True)
    occupation_anglaise = models.CharField(blank=True, max_length=60, null=True)
    facebook  = models.CharField(blank=True, null=False, max_length=60)
    instagram = models.CharField(blank=True, null=False, max_length=60)
    linkedin = models.CharField(blank=True, null=False, max_length=60)
    twitter = models.CharField(blank=True, null=False, max_length=60)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        """
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
        """
    def __str__(self):
        return f' Perfil de {self.user.username}'



class Log(models.Model):
    fecha_hora = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    modelo = models.CharField(max_length=100)
    movimiento = models.CharField(max_length=100)
    mensaje = models.TextField()