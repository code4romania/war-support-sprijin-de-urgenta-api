from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class CustomUser(AbstractUser):
    REQUIRED_FIELDS = []

    USERNAME_FIELD = "email"

    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(_("phone number"), max_length=13, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)

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
