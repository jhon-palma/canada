# Generated by Django 3.2.25 on 2024-08-30 01:19

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_rename_content_post_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='text',
        ),
        migrations.AddField(
            model_name='post',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Content'),
        ),
    ]