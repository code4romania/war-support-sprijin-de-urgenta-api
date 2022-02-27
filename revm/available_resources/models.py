from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from donors.models import Donor

GOODS_CONTAINER_CHOICES = (
    ("BOX", _("Box")),
    ("BOTTLE", _("Bottle")),
)


class ResourceCategory(models.Model):
    name = models.CharField(_("category name"), max_length=50, null=False, blank=False, db_index=True)
    description = models.CharField(_("category description"), default="", blank=True, null=False, max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("resource category")
        verbose_name_plural = _("resource categories")


class ResourceSubcategory(models.Model):
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE)
    name = models.CharField(_("subcategory name"), max_length=50, null=False, blank=False, db_index=True)
    description = models.CharField(_("subcategory description"), default="", blank=True, null=False, max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("resource subcategory")
        verbose_name_plural = _("resource subcategories")


class CommonResource(models.Model):
    subcategory = models.ForeignKey(ResourceSubcategory, on_delete=models.CASCADE)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    name = models.CharField(_("resource name"), max_length=50, null=False, blank=False, db_index=True)
    description = models.CharField(_("resource description"), default="", blank=True, null=False, max_length=500)
    added_on = models.DateTimeField(_("resource added on"), auto_now_add=timezone.now, editable=False)
    available_from = models.DateTimeField(_("resource available from"), auto_now_add=timezone.now, null=False)
    available_until = models.DateTimeField(_("resource available until"), null=True)
    is_finished = models.BooleanField(
        _("resource finished"),
        default=False,
        help_text=_("Is this resource completely used up"),
    )

    def __str__(self):
        return f"{self.subcategory} {self.name}"

    class Meta:
        abstract = True


class CommonLocalizedResource(models.Model):
    COUNTY_CHOICES = list(settings.COUNTIES_SHORTNAME.items())

    county_coverage = models.CharField(_("county"), max_length=2, choices=COUNTY_CHOICES)

    class Meta:
        abstract = True


class CommonReusableResource(CommonResource):
    reuses_left = models.PositiveSmallIntegerField(
        _("reuses left"), help_text=_("How many times can this resource be used"), null=True, blank=True
    )
    is_infinitely_reusable = models.BooleanField(_("is infinitely reusable"), default=False)
    currently_in_use = models.BooleanField(_("reusable resource currently under use"), default=False)
    used_by = models.CharField(_("used by"), max_length=200, null=True, blank=True)

    class Meta:
        abstract = True


class GoodsTransportService(CommonReusableResource, CommonLocalizedResource):
    usable_weight = models.PositiveSmallIntegerField(_("usable weight"), default=0, blank=False)
    has_refrigeration = models.BooleanField(_("has refrigeration"), default=False)


class PeopleTransportService(CommonReusableResource, CommonLocalizedResource):
    total_passengers = models.PositiveSmallIntegerField(_("total passengers"), default=1, blank=False)
    has_disability_access = models.BooleanField(_("has disability access"), default=False)
    has_pet_accommodation = models.BooleanField(_("has pet accommodation"), default=False)


class FoodProductsResource(CommonResource, CommonLocalizedResource):
    unit_type = models.CharField(
        _("unit type"), max_length=10, choices=GOODS_CONTAINER_CHOICES, blank=False, null=False
    )
    total_units = models.PositiveSmallIntegerField(_("total units"), default=0, blank=False)
    expiration_date = models.DateTimeField(_("expiration date"), blank=True, null=True)
    pickup_town = models.CharField(_("pickup town"), max_length=100, blank=False, null=False)
