# Generated by Django 3.2.12 on 2022-03-07 20:04

from django.db import migrations, models
import revm_site.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app_transport_service', '0007_alter_transportserviceoffer_donor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcerequest',
            name='date',
            field=models.DateTimeField(validators=[revm_site.validators.validate_date_disallow_past], verbose_name='transport date'),
        ),
    ]