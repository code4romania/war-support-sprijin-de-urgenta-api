from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from app_account.models import CustomUser
from revm_site.models import CommonCategoryModel


class Category(CommonCategoryModel):
    ...


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(_("subcategory name"), max_length=50, null=False, blank=False, db_index=True)
    description = models.CharField(_("subcategory description"), default="", blank=True, null=False, max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("subcategory")
        verbose_name_plural = _("subcategories")


class OtherOffer(models.Model):
    donor = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(_("resource name"), max_length=100, db_index=True)
    description = models.CharField(_("resource description"), default="", blank=True, null=False, max_length=500)

    added_on = models.DateTimeField(_("resource added on"), auto_now_add=timezone.now, editable=False)
    available_from = models.DateTimeField(_("resource available from"), auto_now_add=timezone.now, null=False)
    available_until = models.DateTimeField(_("resource available until"), null=True)
    expiration_date = models.DateTimeField(_("expiration date"), blank=True, null=True)

    county_coverage = models.CharField(_("county"), max_length=2, choices=settings.COUNTY_CHOICES)
    town = models.CharField(_("town"), max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("other offer")
        verbose_name_plural = _("other offer")


class OtherRequest(models.Model):
    made_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    name = models.CharField(_("name"), max_length=100, db_index=True)
    description = models.CharField(_("description"), default="", blank=True, null=False, max_length=500)

    added_on = models.DateTimeField(_("added on"), auto_now_add=timezone.now, editable=False)

    county_coverage = models.CharField(_("county"), max_length=2, choices=settings.COUNTY_CHOICES)
    town = models.CharField(_("town"), max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("other request")
        verbose_name_plural = _("other requests")


class ResourceRequest(models.Model):
    resource = models.ForeignKey(OtherOffer, on_delete=models.DO_NOTHING)
    request = models.ForeignKey(OtherRequest, on_delete=models.DO_NOTHING)
    # ToDo add here app_item, app_service, app_transport_service, app_volunteering | so we can match them up later

    class Meta:
        verbose_name = _("Offer - Request")
        verbose_name_plural = _("Offer - Request")
