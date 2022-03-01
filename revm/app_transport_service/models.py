from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from app_account.models import CustomUser


TYPES_CHOICES = ((1, _("National")), (2, _("International")))


class Category(models.Model):
    name = models.CharField(_("category name"), max_length=50, null=False, blank=False, db_index=True)
    description = models.CharField(_("category description"), default="", blank=True, null=False, max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(_("subcategory name"), max_length=50, null=False, blank=False, db_index=True)
    description = models.CharField(_("subcategory description"), default="", blank=True, null=False, max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("subcategory")
        verbose_name_plural = _("subcategories")


class TransportServiceResource(models.Model):
    donor = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(_("resource name"), max_length=100, db_index=True)
    description = models.CharField(_("resource description"), default="", blank=True, null=False, max_length=500)

    driver_name = models.CharField(_("driver name"), max_length=255)
    driver_id = models.CharField(_("driver id"), max_length=255)
    car_registration_number = models.CharField(_("car registration number"), max_length=50)

    added_on = models.DateTimeField(_("resource added on"), auto_now_add=timezone.now, editable=False)
    available_from = models.DateTimeField(_("resource available from"), auto_now_add=timezone.now, null=False)
    available_until = models.DateTimeField(_("resource available until"), null=True)
    available_in_weekend = models.BooleanField(default=False)
    available_in_weekday = models.BooleanField(default=False)
    available_anytime = models.BooleanField(default=False)

    county_coverage = models.CharField(_("county coverage"), max_length=2, choices=settings.COUNTY_CHOICES)
    town = models.CharField(_("town"), max_length=100, blank=False, null=False)

    weight_capacity = models.FloatField(blank=True, null=True)
    weight_unit = models.CharField(_("weight unit"), max_length=3, default='kg', blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    volume_unit = models.CharField(_("volume unit"), max_length=3, default='mc', blank=True, null=True)
    has_refrigeration = models.BooleanField(default=False, blank=True, null=True)
    type = models.SmallIntegerField(_("type"), choices=TYPES_CHOICES, default=1, blank=True, null=True)
    available_seats = models.PositiveSmallIntegerField(_("total units"), default=0, blank=True, null=True)
    has_disabled_access = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("service offer")
        verbose_name_plural = _("service offers")


class TransportServiceRequest(models.Model):
    made_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    service_resources = models.ManyToManyField(TransportServiceResource, related_name="service_request")

    name = models.CharField(_("service name"), max_length=100, db_index=True)
    description = models.CharField(_("service description"), default="", blank=True, null=False, max_length=500)

    added_on = models.DateTimeField(_("service added on"), auto_now_add=timezone.now, editable=False)

    county_coverage = models.CharField(_("county"), max_length=2, choices=settings.COUNTY_CHOICES)
    town = models.CharField(_("town"), max_length=100, blank=False, null=False)

    weight_capacity = models.FloatField(blank=True, null=True)
    weight_unit = models.CharField(_("weight unit"), max_length=3, default='kg', blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    volume_unit = models.CharField(_("volume unit"), max_length=3, default='mc', blank=True, null=True)
    has_refrigeration = models.BooleanField(default=False)
    type = models.SmallIntegerField(_("type"), choices=TYPES_CHOICES, default=1, blank=True, null=True)
    available_seats = models.PositiveSmallIntegerField(_("total units"), default=0, blank=True, null=True)
    has_disabled_access = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("service request")
        verbose_name_plural = _("service requests")
