import logging
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from revm_site.settings.base import ITEM_STATUS_COMPLETE

from app_account.models import CustomUser
from revm_site.models import (
    CommonCategoryModel,
    CommonMultipleCountyModel,
    CommonRequestModel,
    CommonOfferModel,
    CommonMultipleLocationModel,
    CommonTransportableModel,
    CommonCountyModel,
    CommonLocationModel
)


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
    expiration_date = models.DateField(_("expiration date"), blank=True, null=True)
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
        return f"#{self.id} {self.name} (Stoc: {self.stock} {self.unit_type}) - {','.join(self.county_coverage)}"

    class Meta:
        verbose_name = _("item offer")
        verbose_name_plural = _("item offers")

    def save(self, *args, **kwargs):
        previous = None
        try:
            previous = ItemOffer.objects.get(pk=self.pk)
        except Exception as e:
            #ToDo: map DoesNotExist execption and tell user
            pass
        self.stock = get_updated_stock_value(previous, self)
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

    class Meta:
        verbose_name = _("item request")
        verbose_name_plural = _("item requests")

    def save(self, *args, **kwargs):
        previous = None
        try:
            previous = ItemRequest.objects.get(pk=self.pk)
        except Exception as e:
            #ToDo: map DoesNotExist execption and tell user
            pass

        self.stock = get_updated_stock_value(previous, self)
        super().save(*args, **kwargs)

#ToDo: handle situation where admin changes total_units
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
        except Exception as e:
            #ToDo: map DoesNotExist execption and tell user
            pass

        requested_amount = self.total_units
        #Matching a request with negative stock is nonsensical.
        if requested_amount < 0:
            #ToDo: notify user
            logger.error("You can't match a request with negative stock. You can give back stock if you've made a mistake by making the numbers reflect reality, but not using negative stock here.")
            return
        #if this is a modificatioon operation. Gotta deal with the delta
        if not (previous is None) and not(previous.total_units is None):
            requested_amount -= previous.total_units

        resource = self.resource
        request = self.request

        if requested_amount > request.stock:
            logger.error("The amount you're trying to transfer {0} is larger than the need {1}".format(requested_amount, request.stock))
            #ToDo: tell user
            return

        if requested_amount > resource.stock:
            logger.error("The amount you're trying to transfer {0} is larger than the available stock {1}".format(requested_amount, resource.stock))
            #ToDo: tell user
            return

        resource.stock -= requested_amount
        request.stock -= requested_amount
        logger.info("Requested {0} Offer Stock remaining:{1} Request stock remaining:{2}".format(requested_amount, resource.stock, request.stock))

        if request.stock == 0:
           request.status = ITEM_STATUS_COMPLETE

        resource.save()
        request.save()

        super().save(*args, **kwargs)


def get_updated_stock_value(previous, current):
    logger = logging.getLogger("django")
    no_previous_record_or_stock = previous is None or current.stock is None or previous.stock is None
    if no_previous_record_or_stock:
        logger.info("Stock initialise {0}".format(current.quantity))
        return current.quantity

    stock = current.stock
    delta = current.quantity - previous.quantity
    stock += delta

    logger.info("Stock delta {delta}. New Stock {stock}. New Quantity {qty}".format(delta=delta, stock=stock, qty=current.quantity))
    if stock < 0:
        stock = 0

    return stock
