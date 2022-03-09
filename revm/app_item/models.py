import logging

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from app_account.models import CustomUser
from revm_site.settings.base import (
    ITEM_STATUS_COMPLETE,
    ITEM_STATUS_VERIFIED,
    ITEM_STATUS_DEACTIVATED,
    ITEM_STATUS_COMPLETE
)

from revm_site.utils.models import (
    CommonCategoryModel,
    CommonMultipleCountyModel,
    CommonRequestModel,
    CommonOfferModel,
    CommonMultipleLocationModel,
    CommonTransportableModel,
    CommonCountyModel,
    CommonLocationModel,
    get_county_coverage_str,
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
    quantity = models.PositiveSmallIntegerField(_("total units"), default=0, blank=False)
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
    kids_age = models.CharField(_("age"), max_length=100, blank=True, null=True)
    other_textiles = models.TextField(_("other"), blank=True, null=True)

    # Corturi
    tent_capacity = models.PositiveSmallIntegerField(_("capacity"), default=0, blank=True, null=False)

    def __str__(self):
        counties_str = get_county_coverage_str(self.county_coverage)
        return f"#{self.id} {self.name} (Stoc: {self.stock} {self.unit_type}) - {counties_str}"

    def fetch_previous(self):
        try:
            return ItemOffer.objects.get(pk=self.pk)
        except ItemOffer.DoesNotExist:
            return None
        raise Exception(_("Failed to communicat with database. Please try again later"))

    class Meta:
        verbose_name = _("item offer")
        verbose_name_plural = _("item offers")

    def save(self, *args, **kwargs):
        previous = self.fetch_previous()
        self.stock = get_stock_value(previous, self)
        validate_item_change(previous, self)
        update_related_fields(self)
        super().save(*args, **kwargs)


class ItemRequest(CommonRequestModel, CommonLocationModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("category"))

    # Descriere produs
    name = models.CharField(_("Product"), max_length=100, db_index=True)

    quantity = models.PositiveSmallIntegerField(_("total units"), default=0, blank=True, null=False)

    packaging_type = models.CharField(_("packaging"), max_length=100, blank=True, null=True)
    unit_type = models.CharField(_("unit type"), max_length=10, blank=False, null=False)

    stock = models.PositiveSmallIntegerField(
        _("Necessary"), help_text=_("How many units are still needed"), null=True, blank=True
    )

    # Textile
    textile_category = models.ForeignKey(
        TextileCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("textile category")
    )
    kids_age = models.CharField(_("age"), max_length=100, blank=True, null=True)
    other_textiles = models.TextField(_("other"), blank=True, null=True)

    # Corturi
    tent_capacity = models.PositiveSmallIntegerField(_("capacity"), default=0, blank=True, null=False)

    def __str__(self):
        str_name = _("Requested")
        return f"#{self.id} {self.name} ({str_name}: {self.stock}/{self.quantity} {self.unit_type})"

    def fetch_previous(self):
        try:
            return ItemRequest.objects.get(pk=self.pk)
        except ItemRequest.DoesNotExist:
            return None
        raise Exception(_("Failed to communicat with database. Please try again later"))

    class Meta:
        verbose_name = _("item request")
        verbose_name_plural = _("item requests")

    def save(self, *args, **kwargs):
        previous = self.fetch_previous()
        self.stock = get_stock_value(previous, self)
        validate_item_change(previous, self)
        update_related_fields(self)
        super().save(*args, **kwargs)


class ResourceRequest(models.Model):
    resource = models.ForeignKey(ItemOffer, on_delete=models.DO_NOTHING, verbose_name=_("donation"))
    request = models.ForeignKey(ItemRequest, on_delete=models.DO_NOTHING, verbose_name=_("request"))

    total_units = models.PositiveSmallIntegerField(_("total units"), default=0, blank=False)
    description = models.TextField(_("description"), default="", blank=True, null=False, max_length=500)

    added_on = models.DateTimeField(_("added on"), auto_now_add=True)

    class Meta:
        verbose_name = _("Offer - Request")
        verbose_name_plural = _("Offer - Request")

    def save(self, *args, **kwargs):
        logger = logging.getLogger("django")
        previous = None
        try:
            previous = ResourceRequest.objects.get(pk=self.pk)
        except ResourceRequest.DoesNotExist:
            pass
        except Exception:
            raise Exception(_("Failed to communicat with database. Please try again later"))

        requested_amount = self.total_units
        #Matching a request with negative stock is nonsensical.
        if requested_amount < 0:
            raise ValidationError(_("You can't match a request with negative stock. You can give back stock if you've made a mistake by making the numbers reflect reality, but not using negative stock here."))

        #if this is a modificatioon operation. Gotta deal with the delta
        if not (previous is None) and not(previous.total_units is None):
            requested_amount -= previous.total_units
            self._restore_amounts_if_connections_changed(previous)

        resource = self.resource
        request = self.request


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
        logger.info(
            "Requested {0} Offer Stock remaining:{1} Request stock remaining:{2}".format(
                requested_amount, resource.stock, request.stock
            )
        )

        #Validate entire set of operations before commiting them (to avoid needing rollbcks)
        validate_item_change(resource.fetch_previous(), resource)
        validate_item_change(request.fetch_previous(), request)

        resource.save()
        request.save()
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.resource.stock += self.total_units
        self.request.stock += self.total_units

        self.resource.save()
        self.request.save()

        super().delete(using, keep_parents)

    def _restore_amounts_if_connections_changed(self, previous):
        if previous.resource.id != self.resource.id:
            previous.resource.stock += previous.total_units
            previous.resource.save()
        elif previous.request.id != self.request.id:
            previous.request.stock += previous.total_units
            previous.request.save()


def get_stock_value(previous, current):
    logger = logging.getLogger("django")

    no_previous_record_or_stock = previous is None or current.stock is None or previous.stock is None
    if no_previous_record_or_stock:
        return current.quantity

    delta = current.quantity - previous.quantity
    stock = current.stock + delta

    logger.info(
        "Stock delta {delta}. New Stock {stock}. New Quantity {qty}".format(
            delta=delta, stock=stock, qty=current.quantity
        )
    )
    if stock < 0:
        stock = 0

    return stock


def validate_item_change(previous, current):
    #new record, is valid by default
    if previous is None:
        return

    if previous.status != ITEM_STATUS_VERIFIED and current.status != ITEM_STATUS_VERIFIED:
        raise ValidationError(_("Item is in incorrect status for the change you're tyring to make"))


def update_related_fields(current):
    if current.stock == 0 and current.status == ITEM_STATUS_VERIFIED:
        current.status = ITEM_STATUS_COMPLETE
