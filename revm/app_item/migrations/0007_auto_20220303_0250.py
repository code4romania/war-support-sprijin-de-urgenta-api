# Generated by Django 3.2.12 on 2022-03-03 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_item', '0006_itemrequest_pickup_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemoffer',
            name='stock',
            field=models.PositiveSmallIntegerField(blank=True, help_text='How many units of this type are left', null=True, verbose_name='Stock'),
        ),
        migrations.AlterField(
            model_name='itemrequest',
            name='stock',
            field=models.PositiveSmallIntegerField(blank=True, help_text='How many units are still needed', null=True, verbose_name='Stock'),
        ),
    ]