# Generated by Django 3.2.12 on 2022-03-03 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_transport_service', '0003_alter_transportservicerequest_available_seats'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transportserviceoffer',
            options={'verbose_name': 'transport service offer', 'verbose_name_plural': 'transport service offers (0)'},
        ),
        migrations.AlterModelOptions(
            name='transportservicerequest',
            options={'verbose_name': 'transport service request', 'verbose_name_plural': 'transport service request (0)'},
        ),
    ]
