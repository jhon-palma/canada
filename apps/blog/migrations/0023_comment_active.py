# Generated by Django 4.2.15 on 2024-09-28 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_alter_article_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]