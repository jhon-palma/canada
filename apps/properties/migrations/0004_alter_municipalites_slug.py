# Generated by Django 3.2.25 on 2024-08-24 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0003_municipalites_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='municipalites',
            name='slug',
            field=models.SlugField(blank=True, max_length=120, null=True, unique=True),
        ),
    ]
