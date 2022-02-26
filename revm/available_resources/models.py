from django.db import models
from django.utils.translation import gettext_lazy as _


class ResourceCategory(models.Model):
    name = models.CharField(_("category name"), max_length=50)
    description = models.CharField(_("category description"), max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("resource category")
        verbose_name_plural = _("resource categories")


class ResourceSubCategory(models.Model):
    name = models.CharField(_("subcategory name"), max_length=50)
    description = models.CharField(_("subcategory description"), max_length=500)

    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("resource category")
        verbose_name_plural = _("resource categories")


class Resource(models.Model):
    name = models.CharField(_("resource name"), max_length=50)
    description = models.TextField(_("resource description"))
    category = models.ForeignKey(ResourceSubCategory, on_delete=models.CASCADE)

    donor_name = models.CharField(_("name"), max_length=255)
    donor_contact_name = models.CharField(_("contact name"), max_length=255, blank=True)
    donor_email = models.EmailField(_("email address"), max_length=255)
    donor_phone_number = models.CharField(_("phone number"), max_length=13, null=True, blank=True)
    donor_county = models.CharField(_("county"), max_length=50, null=True, blank=True)
    donor_details = models.JSONField(_("details"), null=True, blank=True)

    INDIVIDUAL = 0
    COMPANY = 1
    PUBLIC_BODY = 2
    NON_PROFIT = 3
    TYPES = (
        (INDIVIDUAL, _("Individual")),
        (COMPANY, _("Company")),
        (PUBLIC_BODY, _("Public Body")),
        (NON_PROFIT, _("Non-Profit")),
    )

    donor_type = models.SmallIntegerField(_("type"), choices=TYPES, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("resource")
        verbose_name_plural = _("resources")
