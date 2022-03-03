# Generated by Django 3.2.12 on 2022-03-03 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_transport_service', '0004_merge_20220303_0343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resourcerequest',
            name='units',
        ),
        migrations.AlterField(
            model_name='transportserviceoffer',
            name='availability',
            field=models.CharField(choices=[('WK', 'Disponibil in weekend'), ('WD', 'Disponibil in timpul saptamanii'), ('A', 'Disponibil oricand'), ('FI', 'Intervale fixe')], default='WK', max_length=2, verbose_name='availability'),
        ),
        migrations.AlterField(
            model_name='transportserviceoffer',
            name='status',
            field=models.CharField(choices=[('NV', 'Not Verified'), ('V', 'Verified'), ('D', 'Deactivated'), ('C', 'Complete')], default='NV', max_length=5, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='transportservicerequest',
            name='status',
            field=models.CharField(choices=[('NV', 'Not Verified'), ('V', 'Verified'), ('D', 'Deactivated'), ('C', 'Complete')], default='NV', max_length=5, verbose_name='status'),
        ),
    ]
