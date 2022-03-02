from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from app_account.models import CustomUser
from revm_site.models import CommonCategoryModel


class Category(CommonCategoryModel):
    ...


class TextileCategory(CommonCategoryModel):
    ...

    class Meta:
        verbose_name = _("Textile Category")
        verbose_name_plural = _("Textile Categories")

class ItemOffer(models.Model):
    donor = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    description = models.TextField(_("description"), default="", blank=True, null=False)

    # Descriere produs
    name = models.CharField(_("Product"), max_length=100, db_index=True, blank=True, null=False)
    quantity = models.PositiveSmallIntegerField(_("total units"), default=0, blank=False)
    packaging_type = models.CharField(_("packaging"), max_length=100, blank=True, null=True)
    unit_type = models.CharField(_("unit type"), max_length=10, blank=False, null=False)
    expiration_date = models.DateTimeField(_("expiration date"), blank=True, null=True)
    stock = models.PositiveSmallIntegerField(
        _("Stock"), help_text=_("How many units of this type are left"), null=True, blank=True, editable=False
    )

    # Textile
    textile_category = models.ForeignKey(TextileCategory, on_delete=models.CASCADE, null=True, blank=True)
    kids_age = models.CharField(_("age"), max_length=100, blank=True, null=True)
    other_textiles = models.TextField(_("other"), blank=True, null=True)

    # Corturi

    tent_capacity = models.PositiveSmallIntegerField(_("capacity"), default=0, blank=True, null=False)

    county_coverage = models.CharField(_("county"), max_length=2, choices=settings.COUNTY_CHOICES)
    pickup_town = models.CharField(_("pickup town"), max_length=100, blank=False, null=False)

    added_on = models.DateTimeField(_("resource added on"), auto_now_add=timezone.now, editable=False)
    status = models.CharField(
        _("status"), max_length=5, choices=settings.RESOURCE_STATUS, default=settings.RESOURCE_STATUS[0][0]
    )

    def __str__(self):
        return f"#{self.id} {self.name} (Stoc: {self.stock} {self.unit_type})"

    class Meta:
        verbose_name = _("item offer")
        verbose_name_plural = _("item offers")


class ItemRequest(models.Model):
    made_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(_("description"), default="", blank=True, null=False)

    # Descriere produs
    name = models.CharField(_("Product"), max_length=100, db_index=True)

    quantity = models.PositiveSmallIntegerField(_("total units"), default=0, blank=True, null=False)

    packaging_type = models.CharField(_("packaging"), max_length=100, blank=True, null=True)
    unit_type = models.CharField(_("unit type"), max_length=10, blank=False, null=False)
    expiration_date = models.DateTimeField(_("expiration date"), blank=True, null=True)
    stock = models.PositiveSmallIntegerField(
        _("Stock"), help_text=_("How many units are still needed"), null=True, blank=True, editable=False
    )

    # Textile
    textile_category = models.ForeignKey(TextileCategory, on_delete=models.CASCADE, null=True, blank=True)
    kids_age = models.CharField(_("age"), max_length=100, blank=True, null=True)
    other_textiles = models.TextField(_("other"), blank=True, null=True)

    # Corturi
    tent_capacity = models.PositiveSmallIntegerField(_("capacity"), default=0, blank=True, null=False)

    county_coverage = models.CharField(_("county"), max_length=2, choices=settings.COUNTY_CHOICES)
    pickup_town = models.CharField(_("pickup town"), max_length=100, blank=False, null=False)

    added_on = models.DateTimeField(_("resource added on"), auto_now_add=timezone.now, editable=False)

    status = models.CharField(
        _("status"), max_length=5, choices=settings.RESOURCE_STATUS, default=settings.RESOURCE_STATUS[0][0]
    )

    def __str__(self):
        return f"#{self.id} {self.name} (Stoc: {self.stock}/{self.quantity} {self.unit_type})"

    class Meta:
        verbose_name = _("item request")
        verbose_name_plural = _("item requests")


class ResourceRequest(models.Model):
    resource = models.ForeignKey(ItemOffer, on_delete=models.DO_NOTHING)
    request = models.ForeignKey(ItemRequest, on_delete=models.DO_NOTHING)

    total_units = models.PositiveSmallIntegerField(_("total units"), default=0, blank=False)
    description = models.TextField(_("description"), default="", blank=True, null=False, max_length=500)

    added_on = models.DateTimeField(_("added on"), auto_now_add=True)

    class Meta:
        verbose_name = _("Offer - Request")
        verbose_name_plural = _("Offer - Request")

    def save(self, *args, **kwargs):
        # substract amount from offer and request
        resource = self.resource
        request = self.request

        resource.units_left -= self.total_units
        request.units_left -= self.total_units

        resource.save()
        request.save()

        super().save(*args, **kwargs)
