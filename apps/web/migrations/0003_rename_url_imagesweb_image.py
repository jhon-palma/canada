# Generated by Django 3.2.25 on 2024-08-02 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20240802_1801'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagesweb',
            old_name='url',
            new_name='image',
        ),
    ]
