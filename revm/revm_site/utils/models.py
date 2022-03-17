from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from app_account.models import CustomUser
from revm_site.settings.base import ITEM_STATUS_COMPLETE, ITEM_STATUS_VERIFIED


class CommonCategoryModel(models.Model):
    description = models.CharField(_("category description"), default="", blank=True, null=False, max_length=500)
    name = models.CharField(_("category name"), max_length=50, null=False, blank=False, db_index=True)

    name_ro = models.CharField(_("category name (Romanian)"), max_length=50, default=name)
    name_en = models.CharField(_("category name (English)"), max_length=50, default=name)
    name_ru = models.CharField(_("category name (Russian)"), max_length=50, default=name)
    name_uk = models.CharField(_("category name (Ukrainian)"), max_length=50, default=name)

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

    @property
    def person_phone_number(self):
        raise NotImplementedError

    person_phone_number.fget.short_description = _("phone number")

    class Meta:
        abstract = True


class CommonOfferModel(CommonResourceModel):
    donor = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name=_("donor"))
    status = models.CharField(
        _("status"), max_length=5, choices=settings.OFFER_STATUS, default=settings.OFFER_STATUS[0][0]
    )

    @property
    def person_phone_number(self):
        return self.donor.phone_number if self.donor and self.donor.phone_number else "-"

    class Meta:
        abstract = True


class CommonRequestModel(CommonResourceModel):
    made_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name=_("requested by"))
    status = models.CharField(
        _("status"), max_length=5, choices=settings.REQUEST_STATUS, default=settings.REQUEST_STATUS[0][0]
    )

    @property
    def person_phone_number(self):
        return self.made_by.phone_number if self.made_by and self.made_by.phone_number else "-"

    class Meta:
        abstract = True


class CommonResourceRequestModel(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.resource = None
        self.request = None

    def save(self, *args, **kwargs):
        self.request.status = ITEM_STATUS_COMPLETE
        self.resource.status = ITEM_STATUS_COMPLETE
        self.request.save()
        self.resource.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.request.status = ITEM_STATUS_VERIFIED
        self.resource.status = ITEM_STATUS_VERIFIED
        self.request.save()
        self.resource.save()

        super().save(*args, **kwargs)

    class Meta:
        abstract = True


def get_county_coverage_str(county_coverage):
    if len(county_coverage) < len(settings.COUNTY_CHOICES):
        return ",".join(county_coverage)
    elif len(county_coverage) == 0:
        return _("no county")
    return _("all counties")
