# Generated by Django 3.2.12 on 2022-03-04 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_other', '0003_auto_20220304_2259'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='otheroffer',
            options={'verbose_name': 'other offer', 'verbose_name_plural': 'other offers'},
        ),
        migrations.AlterModelOptions(
            name='otherrequest',
            options={'verbose_name': 'other request', 'verbose_name_plural': 'other request'},
        ),
    ]