from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from app_account.models import CustomUser


class CommonCategoryModel(models.Model):
    name = models.CharField(_("category name"), max_length=50, null=False, blank=False, db_index=True)
    description = models.CharField(_("category description"), default="", blank=True, null=False, max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class CommonTransportableModel(models.Model):
    has_transportation = models.BooleanField(_("has transportation"), blank=True, null=True)

    class Meta:
        abstract = True


class CommonMultipleCountyModel(models.Model):
    county_coverage = MultiSelectField(_("county coverage"), choices=settings.COUNTY_CHOICES, blank=True, null=True)

    class Meta:
        abstract = True


class CommonMultipleLocationModel(CommonMultipleCountyModel):
    town = models.CharField(_("town"), max_length=100, blank=True, null=True)

    class Meta:
        abstract = True


class CommonCountyModel(models.Model):
    county_coverage = models.CharField(
        _("county coverage"), choices=settings.COUNTY_CHOICES, max_length=3, blank=True, null=True
    )

    class Meta:
        abstract = True


class CommonLocationModel(CommonCountyModel):
    town = models.CharField(_("town"), max_length=100, blank=True, null=True)

    class Meta:
        abstract = True


class CommonResourceModel(models.Model):
    description = models.CharField(_("description"), default="", blank=True, null=False, max_length=500)

    added_on = models.DateTimeField(_("added on"), auto_now_add=timezone.now, editable=False)
    class Meta:
        abstract = True


class CommonOfferModel(CommonResourceModel):
    donor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("donor"))
    status = models.CharField(
        _("status"), max_length=5, choices=settings.OFFER_STATUS, default=settings.OFFER_STATUS[0][0]
    )


    class Meta:
        abstract = True


class CommonRequestModel(CommonResourceModel):
    made_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("requested by")
    )
    status = models.CharField(
        _("status"), max_length=5, choices=settings.REQUEST_STATUS, default=settings.REQUEST_STATUS[0][0]
    )


    class Meta:
        abstract = True
