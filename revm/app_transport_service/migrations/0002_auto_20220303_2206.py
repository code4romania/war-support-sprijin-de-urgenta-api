# Generated by Django 3.2.12 on 2022-03-03 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_transport_service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportserviceoffer',
            name='weight_unit',
            field=models.CharField(blank=True, default='tone', max_length=10, null=True, verbose_name='weight unit'),
        ),
        migrations.AlterField(
            model_name='transportservicerequest',
            name='weight_unit',
            field=models.CharField(blank=True, default='tone', max_length=10, null=True, verbose_name='weight unit'),
        ),
    ]