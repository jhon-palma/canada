# Generated by Django 5.1.1 on 2024-12-22 23:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_article_meta_description_a_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='meta_description_a',
            new_name='m_description_a',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='meta_description_f',
            new_name='m_description_f',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='meta_title_a',
            new_name='m_title_a',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='meta_title_f',
            new_name='m_title_f',
        ),
    ]
