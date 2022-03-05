from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from app_account.models import CustomUser
from revm_site.models import (
    CommonCountyModel,
    CommonRequestModel,
    CommonOfferModel,
    CommonCategoryModel,
)


class Category(CommonCategoryModel):
    ...


class TransportServiceOffer(CommonCountyModel, CommonOfferModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("category"))

    # Detalii transport marfă
    weight_capacity = models.FloatField(_("Capacity"), blank=True, null=True)
    weight_unit = models.CharField(_("weight unit"), max_length=3, default="t", blank=True, null=True)
    has_refrigeration = models.BooleanField(_("has refrigeration"), default=False, blank=True, null=True)

    # Disponibilitate
    type = models.SmallIntegerField(
        _("type"), choices=settings.TRANSPORT_TYPES_CHOICES, default=1, blank=True, null=True
    )

    availability = models.CharField(
        _("availability"),
        max_length=2,
        choices=settings.TRANSPORT_AVAILABILTY,
        default=settings.TRANSPORT_AVAILABILTY[0][0],
    )
    availability_interval_from = models.TimeField(_("from hour"), null=True, blank=True)
    availability_interval_to = models.TimeField(_("until hour"), null=True, blank=True)

    # Detalii șofer
    driver_name = models.CharField(_("name"), max_length=255)
    driver_contact = models.CharField(_("contact"), max_length=255)
    driver_id = models.CharField(_("id"), max_length=255)
    car_registration_number = models.CharField(_("car registration number"), max_length=50)

    # Detalii transport persoane
    available_seats = models.PositiveSmallIntegerField(_("available seats"), default=0, blank=True, null=True)
    has_disabled_access = models.BooleanField(_("has disabled access"), default=False)
    pets_allowed = models.BooleanField(_("pets allowed"), default=False)

    def __str__(self):
        return f"#{self.id} {self.category}"

    class Meta:
        verbose_name = _("transport service offer")
        verbose_name_plural = _("transport service offers")


class TransportServiceRequest(CommonRequestModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("category"))

    # Detalii transport marfă
    weight_capacity = models.FloatField(_("Capacity"), blank=True, null=True)
    weight_unit = models.CharField(_("weight unit"), max_length=3, default="t", blank=True, null=True)
    has_refrigeration = models.BooleanField(_("has refrigeration"), default=False, blank=True, null=True)

    # Detalii transport persoane
    available_seats = models.PositiveSmallIntegerField(_("available seats"), default=0, blank=True, null=True)
    has_disabled_access = models.BooleanField(_("has disabled access"), default=False)
    pets_allowed = models.BooleanField(_("pets allowed"), default=False)

    # Detalii transport
    from_county = models.CharField(_("From county"), choices=settings.COUNTY_CHOICES, max_length=50)
    from_city = models.CharField(_("From city"), max_length=150)
    to_county = models.CharField(_("To county"), choices=settings.COUNTY_CHOICES, max_length=50)
    to_city = models.CharField(_("From city"), max_length=150)

    def __str__(self):
        return f"#{self.id} {self.category}"

    class Meta:
        verbose_name = _("transport service request")
        verbose_name_plural = _("transport service requests")


class ResourceRequest(models.Model):
    resource = models.ForeignKey(
        TransportServiceOffer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("donation")
    )
    request = models.ForeignKey(
        TransportServiceRequest, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("request")
    )
    date = models.DateTimeField(_("transport date"))
    description = models.TextField(_("description"), default="", blank=True, null=False, max_length=500)

    class Meta:
        verbose_name = _("Offer - Request")
        verbose_name_plural = _("Offer - Request")

    def save(self, *args, **kwargs):
        self.request.status = "C"
        self.request.save()

        super().save(*args, **kwargs)
