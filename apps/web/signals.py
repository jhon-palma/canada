from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .functions import populate_images

@receiver(post_migrate)
def populate_images_on_startup(sender, **kwargs):
    from django.apps import apps
    if sender.name == apps.get_app_config('web').name:
        populate_images()
