# Generated by Django 4.2.15 on 2024-09-28 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_youtube'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='telephone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
