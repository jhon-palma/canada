# Generated by Django 3.2.25 on 2024-08-29 23:54

from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title_anglaise', models.CharField(max_length=255)),
                ('title_francaise', models.CharField(max_length=255)),
                ('slug_francaise', models.SlugField()),
                ('slug_anglaise', models.SlugField()),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ('title_francaise',),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('intro', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('draft', 'Draft')], default='active', max_length=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/blog/images/')),
                ('content', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
                ('slug_francaise', models.SlugField(blank=True, max_length=150, null=True, unique=True)),
                ('slug_anglaise', models.SlugField(blank=True, max_length=150, null=True, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='blog.category')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post')),
            ],
        ),
    ]
