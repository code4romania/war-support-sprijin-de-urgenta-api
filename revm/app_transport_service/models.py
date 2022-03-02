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


class TransportServiceOffer(models.Model):
    donor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(_("name"), max_length=100, db_index=True)
    description = models.CharField(_("description"), default="", blank=True, null=False, max_length=500)

    driver_name = models.CharField(_("driver name"), max_length=255)
    driver_id = models.CharField(_("driver id"), max_length=255)
    car_registration_number = models.CharField(_("car registration number"), max_length=50)

    added_on = models.DateTimeField(_("added on"), auto_now_add=timezone.now, editable=False)
    available_from = models.DateField(_("available from"), null=False)
    available_until = models.DateField(_("available until"), null=True)

    availability = models.CharField(_("availability"), max_length=2,
        choices=settings.TRANSPORT_AVAILABILTY, default=settings.TRANSPORT_AVAILABILTY[0][0])
    availability_interval_from = models.TimeField(_("availability from hour"), null=True, blank=True)
    availability_interval_to = models.TimeField(_("availability until hour"), null=True, blank=True)

    county_coverage = models.CharField(_("county coverage"), max_length=2, choices=settings.COUNTY_CHOICES)
    town = models.CharField(_("town"), max_length=100, blank=False, null=False)

    weight_capacity = models.FloatField(blank=True, null=True)
    weight_unit = models.CharField(_("weight unit"), max_length=3, default="kg", blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    volume_unit = models.CharField(_("volume unit"), max_length=3, default="mc", blank=True, null=True)
    has_refrigeration = models.BooleanField(default=False, blank=True, null=True)

    type = models.SmallIntegerField(_("type"), choices=TYPES_CHOICES, default=1, blank=True, null=True)
    available_seats = models.PositiveSmallIntegerField(_("available seats"), default=0, blank=True, null=True)
    has_disabled_access = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("transport service offer")
        verbose_name_plural = _("transport service offers")


class TransportServiceRequest(models.Model):
    made_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(_("name"), max_length=100, db_index=True)
    description = models.CharField(_("description"), default="", blank=True, null=False, max_length=500)

    added_on = models.DateTimeField(_("added on"), auto_now_add=timezone.now, editable=False)

    county_coverage = models.CharField(_("county"), max_length=2, choices=settings.COUNTY_CHOICES)
    town = models.CharField(_("town"), max_length=100, blank=False, null=False)

    weight_capacity = models.FloatField(blank=True, null=True)
    weight_unit = models.CharField(_("weight unit"), max_length=3, default="kg", blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    volume_unit = models.CharField(_("volume unit"), max_length=3, default="mc", blank=True, null=True)
    has_refrigeration = models.BooleanField(default=False)
    type = models.SmallIntegerField(_("type"), choices=TYPES_CHOICES, default=1, blank=True, null=True)
    available_seats = models.PositiveSmallIntegerField(_("total units"), default=0, blank=True, null=True)
    has_disabled_access = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("transport service request")
        verbose_name_plural = _("transport service requests")


class ResourceRequest(models.Model):
    resource = models.ForeignKey(TransportServiceOffer, on_delete=models.SET_NULL, null=True, blank=True)
    request = models.ForeignKey(TransportServiceRequest, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _("Offer - Request")
        verbose_name_plural = _("Offer - Request")
