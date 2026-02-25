from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db import transaction

from apps.web.models import Formulaire_contact


class Command(BaseCommand):
    help = "Actualiza los campos tag y broker en Formulaire_contact según el sujet"

    @transaction.atomic
    def handle(self, *args, **options):

        self.stdout.write(self.style.WARNING("Iniciando actualización masiva..."))

        total_updates = 0

        updated = Formulaire_contact.objects.filter(
            sujet__iexact="Footer Web"
        ).filter(
            Q(tag__isnull=True) | Q(tag__exact="")
        ).update(tag="Seller")

        total_updates += updated
        self.stdout.write(f"Footer Web actualizados: {updated}")

        updated_tag = Formulaire_contact.objects.filter(
            sujet__iexact="I Want to Buy"
        ).filter(
            Q(tag__isnull=True) | Q(tag__exact="")
        ).update(tag="Buyer")

        updated_broker = Formulaire_contact.objects.filter(
            sujet__iexact="I Want to Buy"
        ).filter(
            Q(broker__isnull=True) | Q(broker__exact="")
        ).update(broker="Booklet Download")

        total_updates += updated_tag + updated_broker
        self.stdout.write(f"I Want to Buy - tag: {updated_tag}, broker: {updated_broker}")

        updated_tag = Formulaire_contact.objects.filter(
            sujet__iexact="I Want to Sell"
        ).filter(
            Q(tag__isnull=True) | Q(tag__exact="")
        ).update(tag="Seller")

        updated_broker = Formulaire_contact.objects.filter(
            sujet__iexact="I Want to Sell"
        ).filter(
            Q(broker__isnull=True) | Q(broker__exact="")
        ).update(broker="Booklet Download")

        total_updates += updated_tag + updated_broker
        self.stdout.write(f"I Want to Sell - tag: {updated_tag}, broker: {updated_broker}")

        updated = Formulaire_contact.objects.filter(
            sujet__iexact="Schedule a visit"
        ).filter(
            Q(tag__isnull=True) | Q(tag__exact="")
        ).update(tag="Buyer")

        total_updates += updated
        self.stdout.write(f"Schedule a visit actualizados: {updated}")

        updated = Formulaire_contact.objects.filter(
            sujet__iexact="Ask more information"
        ).filter(
            Q(tag__isnull=True) | Q(tag__exact="")
        ).update(tag="Buyer")

        total_updates += updated
        self.stdout.write(f"Ask more information actualizados: {updated}")
        
        updated = Formulaire_contact.objects.filter(
            sujet__iexact="Demandez plus d'information"
        ).filter(
            Q(tag__isnull=True) | Q(tag__exact="")
        ).update(tag="Buyer")

        total_updates += updated
        self.stdout.write(f"Demandez plus d'information actualizados: {updated}")
        
        updated = Formulaire_contact.objects.filter(
            sujet__iexact="Planifiez une visite"
        ).filter(
            Q(tag__isnull=True) | Q(tag__exact="")
        ).update(tag="Buyer")

        total_updates += updated
        self.stdout.write(f"Planifiez une visite actualizados: {updated}")
        
        updated = Formulaire_contact.objects.filter(
            sujet__iexact="Contact"
        ).filter(
            Q(tag__isnull=True) | Q(tag__exact="")
        ).update(tag="Contact Us")

        total_updates += updated
        self.stdout.write(f"Contact actualizados: {updated}")
        
        updated = Formulaire_contact.objects.filter(
            sujet__iexact="Evaluation"
        ).filter(
            Q(tag__isnull=True) | Q(tag__exact="")
        ).update(tag="Seller")

        total_updates += updated
        self.stdout.write(f"Evaluation actualizados: {updated}")

        self.stdout.write(self.style.SUCCESS(f"\nActualización completada"))
        self.stdout.write(self.style.SUCCESS(f"Total campos actualizados: {total_updates}"))