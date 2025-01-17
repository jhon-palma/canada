# Generated by Django 3.2.25 on 2024-08-23 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inscriptions',
            options={'ordering': ['devise_prix_demande', '-prix_demande', '-prix_location_demande']},
        ),
        migrations.AddField(
            model_name='quartiers',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
