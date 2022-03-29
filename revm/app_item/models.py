from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from app_account.models import CustomUser
from revm_site.settings.base import ITEM_STATUS_COMPLETE, ITEM_STATUS_VERIFIED
from revm_site.utils.models import (
    CommonCategoryModel,
    CommonMultipleCountyModel,
    CommonRequestModel,
    CommonOfferModel,
    CommonMultipleLocationModel,
    CommonTransportableModel,
    CommonCountyModel,
    CommonLocationModel,
)
from revm_site.utils.validators import validate_date_disallow_past


class Category(CommonCategoryModel):
    ...


class TextileCategory(CommonCategoryModel):
    ...

    class Meta:
        verbose_name = _("Textile Category")
        verbose_name_plural = _("Textile Categories")


class ItemOffer(CommonOfferModel, CommonMultipleLocationModel, CommonTransportableModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("category"))

    # Descriere produs
    name = models.CharField(_("Product"), max_length=100, db_index=True, blank=True, null=False)
    quantity = models.PositiveSmallIntegerField(_("total units"), default=0)
    packaging_type = models.CharField(_("packaging"), max_length=100, blank=True, null=True)
    unit_type = models.CharField(_("unit type"), max_length=10, blank=False, null=False)
    expiration_date = models.DateField(
        _("expiration date"), validators=[validate_date_disallow_past], blank=True, null=True
    )
    stock = models.PositiveSmallIntegerField(
        _("Stock"), help_text=_("How many units of this type are left"), null=True, blank=True
    )

    # Textile
    textile_category = models.ForeignKey(
        TextileCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("textile category")
    )
    textile_size = models.CharField(_("textile size"), max_length=100, blank=True, null=True)
    other_textiles = models.TextField(_("other"), blank=True, null=True)

    # Corturi
    tent_capacity = models.PositiveSmallIntegerField(_("capacity"), default=0, blank=True, null=False)

    def __str__(self):
        counties_str = self.county_coverage_str()
        return f"#{self.id} {self.name} (Stoc: {self.stock} {self.unit_type}) - {counties_str}"

    class Meta:
        verbose_name = _("item offer")
        verbose_name_plural = _("item offers")

    def save(self, *args, **kwargs):
        previous = None
        try:
            previous = ItemOffer.objects.get(pk=self.pk)
        except ItemOffer.DoesNotExist:
            pass

        self.stock = get_stock_value(previous, self)
        super().save(*args, **kwargs)


class ItemRequest(CommonRequestModel, CommonLocationModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("category"))

    # Descriere produs
    name = models.CharField(_("Product"), max_length=100, db_index=True)

    quantity = models.PositiveSmallIntegerField(_("total units"), default=0, blank=True, null=True)

    packaging_type = models.CharField(_("packaging"), max_length=100, blank=True, null=True)
    unit_type = models.CharField(_("unit type"), max_length=10, blank=False, null=False)

    stock = models.PositiveSmallIntegerField(
        _("Necessary"), help_text=_("How many units are still needed"), null=True, blank=True
    )

    # Textile
    textile_category = models.ForeignKey(
        TextileCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("textile category")
    )
    textile_size = models.CharField(_("textile size"), max_length=100, blank=True, null=True)
    other_textiles = models.TextField(_("other"), blank=True, null=True)

    # Corturi
    tent_capacity = models.PositiveSmallIntegerField(_("capacity"), default=0, blank=True, null=False)

    def __str__(self):
        str_name = _("Requested")
        return f"#{self.id} {self.name} ({str_name}: {self.stock}/{self.quantity} {self.unit_type})"

    class Meta:
        verbose_name = _("item request")
        verbose_name_plural = _("item requests")

    def save(self, *args, **kwargs):
        previous = None
        try:
            previous = ItemRequest.objects.get(pk=self.pk)
        except ItemRequest.DoesNotExist:
            pass

        self.stock = get_stock_value(previous, self)
        super().save(*args, **kwargs)


class ResourceRequest(models.Model):
    resource = models.ForeignKey(ItemOffer, on_delete=models.DO_NOTHING, verbose_name=_("donation"))
    request = models.ForeignKey(ItemRequest, on_delete=models.DO_NOTHING, verbose_name=_("request"))

    total_units = models.PositiveSmallIntegerField(_("total units"), default=0, blank=False)
    description = models.TextField(_("description"), default="", blank=True, null=False, max_length=500)

    added_on = models.DateTimeField(_("added on"), auto_now_add=timezone.now)

    class Meta:
        verbose_name = _("Offer - Request")
        verbose_name_plural = _("Offer - Request")

    def save(self, *args, **kwargs):
        previous = None
        try:
            previous = ResourceRequest.objects.get(pk=self.pk)
        except ResourceRequest.DoesNotExist:
            pass

        requested_amount = self.total_units

        if not (previous is None) and not (previous.total_units is None):
            requested_amount -= previous.total_units
            self._restore_amounts_if_connections_changed(previous)

        resource = ItemOffer.objects.get(pk=self.resource.id)
        request = ItemRequest.objects.get(pk=self.request.id)

        if requested_amount > request.stock:
            raise ValidationError(
                _(
                    f"The amount you're trying to transfer {requested_amount} "
                    f"is larger than the need {request.stock}."
                )
            )

        if requested_amount > resource.stock:
            raise ValidationError(
                _(
                    f"The amount you're trying to transfer {requested_amount} "
                    f"is larger than the available stock {resource.stock}."
                )
            )

        resource.stock -= requested_amount
        request.stock -= requested_amount

        if resource.stock == 0:
            resource.status = ITEM_STATUS_COMPLETE
        if request.stock == 0:
            request.status = ITEM_STATUS_COMPLETE

        resource.save()
        request.save()

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.resource.stock += self.total_units
        self.request.stock += self.total_units

        self.resource.status = ITEM_STATUS_VERIFIED
        self.request.status = ITEM_STATUS_VERIFIED

        self.resource.save()
        self.request.save()

        super().delete(using, keep_parents)

    def _restore_amounts_if_connections_changed(self, previous):
        if previous.resource.id != self.resource.id:
            previous.resource.stock += previous.total_units
            previous.resource.status = ITEM_STATUS_VERIFIED
            previous.resource.save()
        elif previous.request.id != self.request.id:
            previous.request.stock += previous.total_units
            previous.request.status = ITEM_STATUS_VERIFIED
            previous.request.save()


def get_stock_value(previous, current):
    no_previous_record_or_stock = previous is None or current.stock is None or previous.stock is None
    if no_previous_record_or_stock:
        return current.quantity

    delta = current.quantity - previous.quantity
    stock = current.stock + delta

    if stock < 0:
        stock = 0

    return stock
