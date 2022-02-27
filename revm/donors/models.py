from django.db import models
from django.utils.translation import gettext_lazy as _


class Donor(models.Model):
    CHOICES = ((1, _("Individual")), (2, _("Corporate")), (3, _("Non-Profit")), (4, _("Government")))

    name = models.CharField(_("name"), max_length=255)
    contact_name = models.CharField(_("contact name"), max_length=255, blank=True)
    email = models.EmailField(_("email address"), max_length=255)
    phone_number = models.CharField(_("phone number"), max_length=13, null=True, blank=True)
    type = models.SmallIntegerField(_("type"), choices=CHOICES, default=1)
    details = models.JSONField(_("details"), null=True, blank=True)

    def __str__(self):
        return self.name
