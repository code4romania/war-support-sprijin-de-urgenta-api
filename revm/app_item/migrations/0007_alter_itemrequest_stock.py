# Generated by Django 3.2.12 on 2022-03-07 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_item', '0006_auto_20220307_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemrequest',
            name='stock',
            field=models.PositiveSmallIntegerField(blank=True, help_text='How many units are still needed', null=True, verbose_name='Necessary'),
        ),
    ]
