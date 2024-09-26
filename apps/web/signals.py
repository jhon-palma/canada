
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from scripts.send_email import sendEmail
from .models import *


@receiver(post_save, sender=Formulaire_contact)
def post_save_formulaire_contact(sender, instance, **kwargs):
    subject = '🔰 YOU HAVE RECEIVED AN LEAD --> {}'.format(instance.sujet.upper)
    date = '📅 Date: {}\n'.format(str(instance.date_creation)[:19])
    name = '👔 Names: {}\n'.format(instance.nom)
    email = '✉️ Email: {}\n'.format(instance.courriel)
    telephone = '📲 Telephone: {}\n\n'.format(instance.telephone)
    origin = '🔍 Origin: {}\n'.format(instance.sujet)
    content = '{}{}{}{}{}'.format(date, name, email, telephone, origin)
    sendEmail('mar@ljrealties.com', 'info@ljrealties.com', subject, content)




