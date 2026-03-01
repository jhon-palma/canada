from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db import transaction
import re
from apps.web.models import Formulaire_contact


class Command(BaseCommand):
    help = "Actualiza los campos tag y broker en Formulaire_contact según el sujet"

    @transaction.atomic
    def handle(self, *args, **options):

        self.stdout.write(self.style.WARNING("Limpiando campo sujet..."))

        records = Formulaire_contact.objects.all().only("id", "sujet")

        cleaned_count = 0

        for obj in records.iterator():
            original = obj.sujet or ""

            cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", original)

            cleaned = re.sub(r"\s+", " ", cleaned).strip()

            if cleaned != original:
                Formulaire_contact.objects.filter(id=obj.id).update(sujet=cleaned)
                cleaned_count += 1

        self.stdout.write(self.style.SUCCESS(f"Registros limpiados: {cleaned_count}"))

        self.stdout.write(self.style.WARNING("Iniciando actualización masiva..."))

        total_updates = 0

        updated = Formulaire_contact.objects.filter(
            sujet__iexact="Footer Web"
        ).filter(
            Q(tags__isnull=True) | Q(tags=[])
        ).update(tags=["Seller"])

        total_updates += updated
        self.stdout.write(f"Footer Web actualizados: {updated}")

        updated_tag = Formulaire_contact.objects.filter(
            sujet__iexact="Book a Call with Us"
        ).filter(
            Q(tags__isnull=True) | Q(tags=[])
        ).update(tags=["Buyer", "Consultation Request"])

        total_updates += updated_tag 
        self.stdout.write(f"Book a Call with Us - tags: {updated_tag}")

        updated_tag = Formulaire_contact.objects.filter(
            sujet__iexact="I Want to Buy"
        ).filter(
            Q(tags__isnull=True) | Q(tags=[])
        ).update(tags=["Buyer", "Booklet Download"])

        total_updates += updated_tag 
        self.stdout.write(f"I Want to Buy - tags: {updated_tag}")
        
        updated_tag = Formulaire_contact.objects.filter(
            sujet__iexact="I Want to Sell"
        ).filter(
            Q(tags__isnull=True) | Q(tags=[])
        ).update(tags=["Seller", "Booklet Download"])

        total_updates += updated_tag 
        self.stdout.write(f"I Want to Sell - tags: {updated_tag}")

        updated_tag = Formulaire_contact.objects.filter(
            sujet__iexact="Schedule a visit"
        ).filter(
            Q(tags__isnull=True) | Q(tags=[])
        ).update(tags=["Buyer"])

        total_updates += updated_tag 
        self.stdout.write(f"Schedule a visit - tags: {updated_tag}")

        updated = Formulaire_contact.objects.filter(
            sujet__iexact="Schedule a visit"
        ).filter(
            Q(broker__isnull=True) | Q(broker__exact="")
        ).update(broker="LJ Aguinaga")

        total_updates += updated
        self.stdout.write(f"Schedule a visit actualizados: {updated}")

        updated_tag = Formulaire_contact.objects.filter(
            sujet__iexact="Button properties"
        ).filter(
            Q(tags__isnull=True) | Q(tags=[])
        ).update(tags=["Buyer"])

        total_updates += updated_tag 
        self.stdout.write(f"Button properties - tags: {updated_tag}")

        updated = Formulaire_contact.objects.filter(
            sujet__iexact="Button properties"
        ).filter(
            Q(broker__isnull=True) | Q(broker__exact="")
        ).update(broker="LJ Aguinaga")

        total_updates += updated
        self.stdout.write(f"Button properties actualizados: {updated}")

        updated_tag = Formulaire_contact.objects.filter(
            sujet__iexact="Ask more information"
        ).filter(
            Q(tags__isnull=True) | Q(tags=[])
        ).update(tags=["Buyer"])

        total_updates += updated_tag 
        self.stdout.write(f"Ask more information - tags: {updated_tag}")
        
        updated = Formulaire_contact.objects.filter(
            sujet__iexact="Ask more information"
        ).filter(
            Q(broker__isnull=True) | Q(broker__exact="")
        ).update(broker="LJ Aguinaga")

        total_updates += updated
        self.stdout.write(f"Ask more information actualizados: {updated}")
        
        updated_tag = Formulaire_contact.objects.filter(
            sujet__iexact="Demandez plus d'information"
        ).filter(
            Q(tags__isnull=True) | Q(tags=[])
        ).update(tags=["Buyer"])

        total_updates += updated_tag 
        self.stdout.write(f"Demandez plus d'information - tags: {updated_tag}")
        
        updated = Formulaire_contact.objects.filter(
            sujet__iexact="Planifiez une visite"
        ).filter(
            Q(tags__isnull=True) | Q(tags=[])
        ).update(tags=["Buyer"])

        total_updates += updated
        self.stdout.write(f"Planifiez une visite actualizados: {updated}")
        
        updated = Formulaire_contact.objects.filter(
            sujet__iexact="Contact"
        ).filter(
            Q(tags__isnull=True) | Q(tags=[])
        ).update(tags=["Contact Us"])

        total_updates += updated
        self.stdout.write(f"Contact actualizados: {updated}")
        
        updated = Formulaire_contact.objects.filter(
            sujet__iexact="Evaluation"
        ).filter(
            Q(tags__isnull=True) | Q(tags=[])
        ).update(tags=["Seller"])

        total_updates += updated
        self.stdout.write(f"Evaluation actualizados: {updated}")
        
        updated = Formulaire_contact.objects.filter(
            sujet__iexact="Banner Get Offer"
        ).filter(
            Q(tags__isnull=True) | Q(tags=[])
        ).update(tags=["Buyer"])

        total_updates += updated
        self.stdout.write(f"Banner Get Offer actualizados: {updated}")
        
        updated = Formulaire_contact.objects.filter(
            sujet__iexact="Request more information"
        ).filter(
            Q(tags__isnull=True) | Q(tags=[])
        ).update(tags=["Buyer"])

        total_updates += updated
        self.stdout.write(f"Request more information actualizados: {updated}")
        
        updated = Formulaire_contact.objects.filter(
            sujet__iexact="Plan a visit"
        ).filter(
            Q(tags__isnull=True) | Q(tags=[])
        ).update(tags=["Buyer"])

        total_updates += updated
        self.stdout.write(f"Plan a visit actualizados: {updated}")

        allowed_sujets = [
            "Ask more information",
            "Banner Get Offer",
            "Book a buyers consultation",
            "Book a Call with Us",
            "Button properties",
            "Contact",
            "Demandez plus dinformation",
            "Evaluation",
            "Footer Web",
            "I Want to Buy",
            "I Want to Sell",
            "Planifiez une visite",
            "Schedule a visit",
        ]
        
        updated = Formulaire_contact.objects.exclude(
            sujet__in=allowed_sujets
        ).update(sujet="Footer Web")

        total_updates += updated
        self.stdout.write(f"Sujet normalizados a 'Footer Web': {updated}")
        
        self.stdout.write(self.style.SUCCESS(f"\nActualización completada"))
        self.stdout.write(self.style.SUCCESS(f"Total campos actualizados: {total_updates}"))