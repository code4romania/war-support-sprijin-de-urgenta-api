# Generated by Django 3.2.12 on 2022-03-07 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_item', '0004_auto_20220305_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemrequest',
            name='county_coverage',
            field=models.CharField(blank=True, choices=[('AB', 'Alba'), ('AR', 'Arad'), ('AG', 'Argeș'), ('BC', 'Bacău'), ('BH', 'Bihor'), ('BN', 'Bistrița-Năsăud'), ('BT', 'Botoșani'), ('BV', 'Brașov'), ('BR', 'Brăila'), ('B', 'București'), ('BZ', 'Buzău'), ('CL', 'Călărași'), ('CS', 'Caraș-Severin'), ('CJ', 'Cluj'), ('CT', 'Constanța'), ('CV', 'Covasna'), ('DB', 'Dâmbovița'), ('DJ', 'Dolj'), ('GL', 'Galați'), ('GR', 'Giurgiu'), ('GJ', 'Gorj'), ('HR', 'Harghita'), ('HD', 'Hunedoara'), ('IL', 'Ialomița'), ('IS', 'Iași'), ('IF', 'Ilfov'), ('MM', 'Maramureș'), ('MH', 'Mehedinți'), ('MS', 'Mureș'), ('NT', 'Neamț'), ('OT', 'Olt'), ('PH', 'Prahova'), ('SM', 'Satu Mare'), ('SJ', 'Sălaj'), ('SB', 'Sibiu'), ('SV', 'Suceava'), ('TR', 'Teleorman'), ('TM', 'Timiș'), ('TL', 'Tulcea'), ('VS', 'Vaslui'), ('VL', 'Vâlcea'), ('VN', 'Vrancea')], max_length=3, null=True, verbose_name='county coverage'),
        ),
    ]
