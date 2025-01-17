# Generated by Django 5.1.1 on 2024-09-17 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_alter_comment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image_anglaise',
            field=models.ImageField(blank=True, default='public/web/blog/images/default.png', null=True, upload_to='public/web/blog/images/'),
        ),
        migrations.AlterField(
            model_name='article',
            name='image_francaise',
            field=models.ImageField(blank=True, default='public/web/blog/images/default.png', null=True, upload_to='public/web/blog/images/'),
        ),
    ]
