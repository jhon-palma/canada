# Generated by Django 4.2.11 on 2024-06-04 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscriptions',
            name='courtier_inscripteur_1',
            field=models.ForeignKey(blank=True, db_column='COURTIER_INSCRIPTEUR_1', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inscriptions_courtier_1', to='properties.membres', to_field='code'),
        ),
        migrations.AlterField(
            model_name='inscriptions',
            name='courtier_inscripteur_2',
            field=models.ForeignKey(blank=True, db_column='COURTIER_INSCRIPTEUR_2', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inscriptions_courtier_2', to='properties.membres', to_field='code'),
        ),
    ]