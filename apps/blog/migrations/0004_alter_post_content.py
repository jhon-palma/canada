# Generated by Django 3.2.25 on 2024-08-30 01:54

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20240829_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True),
        ),
    ]