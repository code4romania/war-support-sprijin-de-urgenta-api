from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from app_account.models import CustomUser
from revm_site.models import CommonRequestModel, CommonCountyModel, CommonOfferModel, CommonLocationModel


class Type(models.Model):
    name = models.CharField(_("type name"), max_length=50, null=False, blank=False, db_index=True)
    description = models.CharField(_("type description"), default="", blank=True, null=False, max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("volunteering type")
        verbose_name_plural = _("volunteering types")


class VolunteeringOffer(CommonOfferModel, CommonLocationModel):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name=_("type"))

    available_from = models.DateTimeField(_("volunteer available from"), auto_now_add=timezone.now, null=False)
    available_until = models.DateTimeField(_("volunteer available until"), null=True)

    def __str__(self):
        return self.type.name

    class Meta:
        verbose_name = _("volunteering offer")
        verbose_name_plural = _("volunteering offers")


class VolunteeringRequest(CommonRequestModel, CommonLocationModel):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name=_("type"))

    def __str__(self):
        return self.type.name

    class Meta:
        verbose_name = _("volunteering request")
        verbose_name_plural = _("volunteering requests")


class ResourceRequest(models.Model):
    resource = models.ForeignKey(VolunteeringOffer, on_delete=models.DO_NOTHING, verbose_name=_("made_by"))
    request = models.ForeignKey(VolunteeringRequest, on_delete=models.DO_NOTHING, verbose_name=_("type"))

    class Meta:
        verbose_name = _("Offer - Request")
        verbose_name_plural = _("Offer - Request")
