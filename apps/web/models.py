import uuid
from django.db import models

class Formulaire_contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    no_formulaire = models.IntegerField()  
    nom = models.CharField(max_length=100, blank=True, null=True)
    courriel = models.EmailField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    adresse = models.CharField(max_length=255,blank=True, null=True)
    sujet = models.CharField(max_length=100)
    read = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_lecture = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.no_formulaire:
            last_instance = Formulaire_contact.objects.order_by('-no_formulaire').first()
            if last_instance:
                self.no_formulaire = last_instance.no_formulaire + 1
            else:
                self.no_formulaire = 1
        super(Formulaire_contact, self).save(*args, **kwargs)