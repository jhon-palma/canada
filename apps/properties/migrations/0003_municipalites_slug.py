# Generated by Django 3.2.25 on 2024-08-24 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_auto_20240823_0628'),
    ]

    operations = [
        migrations.AddField(
            model_name='municipalites',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
