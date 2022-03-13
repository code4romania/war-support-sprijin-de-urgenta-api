from django.db import models
from django.utils.translation import gettext_lazy as _

from app_account.models import CustomUser
from revm_site.utils.models import (
    CommonRequestModel,
    CommonMultipleCountyModel,
    CommonOfferModel,
    CommonMultipleLocationModel,
    CommonTransportableModel,
    CommonLocationModel,
    get_county_coverage_str,
    CommonResourceRequestModel,
)
from revm_site.utils.validators import validate_date_disallow_past


class Type(models.Model):
    name = models.CharField(_("type name"), max_length=50, null=False, blank=False, db_index=True)
    description = models.CharField(_("type description"), default="", blank=True, null=False, max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("volunteering type")
        verbose_name_plural = _("volunteering types")


class VolunteeringOffer(CommonOfferModel, CommonMultipleLocationModel, CommonTransportableModel):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name=_("type"))

    name = models.CharField(_("name"), max_length=100, null=False, blank=False)
    available_until = models.DateField(
        _("volunteer available until"), validators=[validate_date_disallow_past], null=True
    )

    def __str__(self):
        counties_str = get_county_coverage_str(self.county_coverage)
        return f"#{self.pk} {self.type.name} {self.town}({counties_str})"

    class Meta:
        verbose_name = _("volunteering offer")
        verbose_name_plural = _("volunteering offers")


class VolunteeringRequest(CommonRequestModel, CommonLocationModel):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name=_("type"))

    def __str__(self):
        counties_str = get_county_coverage_str(self.county_coverage)
        return f"#{self.pk} {self.type.name} {self.town}({counties_str})"

    class Meta:
        verbose_name = _("volunteering request")
        verbose_name_plural = _("volunteering request")


class ResourceRequest(CommonResourceRequestModel):
    resource = models.ForeignKey(VolunteeringOffer, on_delete=models.DO_NOTHING, verbose_name=_("made_by"))
    request = models.ForeignKey(VolunteeringRequest, on_delete=models.DO_NOTHING, verbose_name=_("type"))

    class Meta:
        verbose_name = _("Offer - Request")
        verbose_name_plural = _("Offer - Request")
