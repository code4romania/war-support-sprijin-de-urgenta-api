from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class CustomUser(AbstractUser):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    TYPES_CHOICES = ((1, _("Individual")), (2, _("Corporate")), (3, _("Non-Profit")), (4, _("Government")))

    business_name = models.CharField(_("bussiness name"), max_length=255, null=True, blank=True)
    identification_no = models.CharField(_("identification number"), max_length=25, null=True, blank=True)

    email = models.EmailField(_("email address"), unique=True)

    type = models.SmallIntegerField(_("type"), choices=TYPES_CHOICES, default=1)
    phone_number = models.CharField(_("phone number"), max_length=13, null=True, blank=True)
    address = models.CharField(_("address"), max_length=255, blank=True, null=True)
    details = models.JSONField(_("details"), null=True, blank=True)
    description = models.CharField(_("general user description"), default="", blank=True, null=False, max_length=500)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        self.username = self.email
        super(CustomUser, self).save(*args, **kwargs)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
