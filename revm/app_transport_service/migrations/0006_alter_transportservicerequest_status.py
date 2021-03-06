# Generated by Django 3.2.12 on 2022-03-07 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_transport_service', '0005_auto_20220305_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportservicerequest',
            name='status',
            field=models.CharField(choices=[('NV', 'Not Verified'), ('V', 'Verified'), ('D', 'Deactivated'), ('C', 'Solved')], default='NV', max_length=5, verbose_name='status'),
        ),
    ]
