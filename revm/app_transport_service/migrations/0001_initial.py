# Generated by Django 3.2.12 on 2022-03-01 21:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='category name')),
                ('description', models.CharField(blank=True, default='', max_length=500, verbose_name='category description')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='subcategory name')),
                ('description', models.CharField(blank=True, default='', max_length=500, verbose_name='subcategory description')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_transport_service.category')),
            ],
            options={
                'verbose_name': 'subcategory',
                'verbose_name_plural': 'subcategories',
            },
        ),
        migrations.CreateModel(
            name='TransportServiceResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='resource name')),
                ('description', models.CharField(blank=True, default='', max_length=500, verbose_name='resource description')),
                ('driver_name', models.CharField(max_length=255, verbose_name='driver name')),
                ('driver_id', models.CharField(max_length=255, verbose_name='driver id')),
                ('car_registration_number', models.CharField(max_length=50, verbose_name='car registration number')),
                ('added_on', models.DateTimeField(auto_now_add=True, verbose_name='resource added on')),
                ('available_from', models.DateTimeField(auto_now_add=True, verbose_name='resource available from')),
                ('available_until', models.DateTimeField(null=True, verbose_name='resource available until')),
                ('available_in_weekend', models.BooleanField(default=False)),
                ('available_in_weekday', models.BooleanField(default=False)),
                ('available_anytime', models.BooleanField(default=False)),
                ('county_coverage', models.CharField(choices=[('AB', 'Alba'), ('AR', 'Arad'), ('AG', 'Argeș'), ('BC', 'Bacău'), ('BH', 'Bihor'), ('BN', 'Bistrița-Năsăud'), ('BT', 'Botoșani'), ('BV', 'Brașov'), ('BR', 'Brăila'), ('B', 'București'), ('BZ', 'Buzău'), ('CL', 'Călărași'), ('CS', 'Caraș-Severin'), ('CJ', 'Cluj'), ('CT', 'Constanța'), ('CV', 'Covasna'), ('DB', 'Dâmbovița'), ('DJ', 'Dolj'), ('GL', 'Galați'), ('GR', 'Giurgiu'), ('GJ', 'Gorj'), ('HR', 'Harghita'), ('HD', 'Hunedoara'), ('IL', 'Ialomița'), ('IS', 'Iași'), ('IF', 'Ilfov'), ('MM', 'Maramureș'), ('MH', 'Mehedinți'), ('MS', 'Mureș'), ('NT', 'Neamț'), ('OT', 'Olt'), ('PH', 'Prahova'), ('SM', 'Satu Mare'), ('SJ', 'Sălaj'), ('SB', 'Sibiu'), ('SV', 'Suceava'), ('TR', 'Teleorman'), ('TM', 'Timiș'), ('TL', 'Tulcea'), ('VS', 'Vaslui'), ('VL', 'Vâlcea'), ('VN', 'Vrancea'), ('RO', 'Național')], max_length=2, verbose_name='county coverage')),
                ('town', models.CharField(max_length=100, verbose_name='town')),
                ('weight_capacity', models.FloatField(blank=True, null=True)),
                ('weight_unit', models.CharField(blank=True, default='kg', max_length=3, null=True, verbose_name='weight unit')),
                ('volume', models.FloatField(blank=True, null=True)),
                ('volume_unit', models.CharField(blank=True, default='mc', max_length=3, null=True, verbose_name='volume unit')),
                ('has_refrigeration', models.BooleanField(blank=True, default=False, null=True)),
                ('type', models.SmallIntegerField(blank=True, choices=[(1, 'National'), (2, 'International')], default=1, null=True, verbose_name='type')),
                ('available_seats', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='total units')),
                ('has_disabled_access', models.BooleanField(default=False)),
                ('pets_allowed', models.BooleanField(default=False)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_transport_service.subcategory')),
            ],
            options={
                'verbose_name': 'service offer',
                'verbose_name_plural': 'service offers',
            },
        ),
        migrations.CreateModel(
            name='TransportServiceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='service name')),
                ('description', models.CharField(blank=True, default='', max_length=500, verbose_name='service description')),
                ('added_on', models.DateTimeField(auto_now_add=True, verbose_name='service added on')),
                ('county_coverage', models.CharField(choices=[('AB', 'Alba'), ('AR', 'Arad'), ('AG', 'Argeș'), ('BC', 'Bacău'), ('BH', 'Bihor'), ('BN', 'Bistrița-Năsăud'), ('BT', 'Botoșani'), ('BV', 'Brașov'), ('BR', 'Brăila'), ('B', 'București'), ('BZ', 'Buzău'), ('CL', 'Călărași'), ('CS', 'Caraș-Severin'), ('CJ', 'Cluj'), ('CT', 'Constanța'), ('CV', 'Covasna'), ('DB', 'Dâmbovița'), ('DJ', 'Dolj'), ('GL', 'Galați'), ('GR', 'Giurgiu'), ('GJ', 'Gorj'), ('HR', 'Harghita'), ('HD', 'Hunedoara'), ('IL', 'Ialomița'), ('IS', 'Iași'), ('IF', 'Ilfov'), ('MM', 'Maramureș'), ('MH', 'Mehedinți'), ('MS', 'Mureș'), ('NT', 'Neamț'), ('OT', 'Olt'), ('PH', 'Prahova'), ('SM', 'Satu Mare'), ('SJ', 'Sălaj'), ('SB', 'Sibiu'), ('SV', 'Suceava'), ('TR', 'Teleorman'), ('TM', 'Timiș'), ('TL', 'Tulcea'), ('VS', 'Vaslui'), ('VL', 'Vâlcea'), ('VN', 'Vrancea'), ('RO', 'Național')], max_length=2, verbose_name='county')),
                ('town', models.CharField(max_length=100, verbose_name='town')),
                ('weight_capacity', models.FloatField(blank=True, null=True)),
                ('weight_unit', models.CharField(blank=True, default='kg', max_length=3, null=True, verbose_name='weight unit')),
                ('volume', models.FloatField(blank=True, null=True)),
                ('volume_unit', models.CharField(blank=True, default='mc', max_length=3, null=True, verbose_name='volume unit')),
                ('has_refrigeration', models.BooleanField(default=False)),
                ('type', models.SmallIntegerField(blank=True, choices=[(1, 'National'), (2, 'International')], default=1, null=True, verbose_name='type')),
                ('available_seats', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='total units')),
                ('has_disabled_access', models.BooleanField(default=False)),
                ('pets_allowed', models.BooleanField(default=False)),
                ('made_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('service_resources', models.ManyToManyField(related_name='service_request', to='app_transport_service.TransportServiceResource')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_transport_service.subcategory')),
            ],
            options={
                'verbose_name': 'service request',
                'verbose_name_plural': 'service requests',
            },
        ),
    ]