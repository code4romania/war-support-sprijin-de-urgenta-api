from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from app_account.models import CustomUser


class Type(models.Model):
    name = models.CharField(_("type name"), max_length=50, null=False, blank=False, db_index=True)
    description = models.CharField(_("type description"), default="", blank=True, null=False, max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("volunteering type")
        verbose_name_plural = _("volunteering types")


class VolunteeringResource(models.Model):
    donor = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    description = models.CharField(_("resource description"), default="", blank=True, null=False, max_length=500)

    county_coverage = models.CharField(_("county"), max_length=2, choices=settings.COUNTY_CHOICES)
    town = models.CharField(_("town"), max_length=100, blank=False, null=False)

    added_on = models.DateTimeField(_("resource added on"), auto_now_add=timezone.now, editable=False)
    available_from = models.DateTimeField(_("resource available from"), auto_now_add=timezone.now, null=False)
    available_until = models.DateTimeField(_("resource available until"), null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("volunteering offer")
        verbose_name_plural = _("volunteering offers")


class VolunteeringRequest(models.Model):
    made_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    volunteering_resources = models.ManyToManyField(VolunteeringResource, related_name="volunteering_request")

    description = models.CharField(_("resource description"), default="", blank=True, null=False, max_length=500)
    county_coverage = models.CharField(_("county"), max_length=2, choices=settings.COUNTY_CHOICES)
    town = models.CharField(_("town"), max_length=100, blank=False, null=False)
    added_on = models.DateTimeField(_("resource added on"), auto_now_add=timezone.now, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("volunteering request")
        verbose_name_plural = _("volunteering requests")
