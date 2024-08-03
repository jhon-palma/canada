from django.db import models
from apps.accounts.models import CustomUser
from apps.properties.models import Membres
from apps.parametrization.models import TypeUser
import uuid



def user_photo_directory_path(instance, filename):
    path = 'profile_imgs/{}'.format(filename)
    return path



class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_imgs/default.png', upload_to=user_photo_directory_path)
    image_over = models.ImageField(default='profile_imgs/default_over.png', upload_to=user_photo_directory_path)
    order = models.SmallIntegerField(blank=True, null=True)
    membre = models.ForeignKey(Membres, on_delete=models.CASCADE, blank=True, null=True)
    type = models.ManyToManyField(TypeUser, through='ProfileTypeUser', related_name='type_users', blank=True)
    occupation = models.CharField(blank=True, max_length=60, null=True)
    occupation_anglaise = models.CharField(blank=True, max_length=60, null=True)
    facebook  = models.CharField(blank=True, null=False, max_length=60)
    instagram = models.CharField(blank=True, null=False, max_length=60)
    linkedin = models.CharField(blank=True, null=False, max_length=60)
    twitter = models.CharField(blank=True, null=False, max_length=60)
    tiktok = models.CharField(blank=True, null=False, max_length=60)
    presentation_f = models.CharField(max_length=2000, blank=True, null=True)  
    presentation_a = models.CharField(max_length=2000, blank=True, null=True)  

    def __str__(self):
        return f' Perfil de {self.user.username}'



class ProfileTypeUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE)
    type = models.ForeignKey(TypeUser, null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'profile_type_user'
        verbose_name = 'profile_type_user'



class Log(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    modelo = models.CharField(max_length=100)
    movimiento = models.CharField(max_length=100)
    mensaje = models.TextField()