from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _

USERS_GROUP = "Users"
CJCCI_GROUP = "CJCCI"
CNCCI_GROUP = "CNCCI"


class CustomUser(AbstractUser):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    INDIVIDUAL = 1
    CORPORATE = 2
    NON_PROFIT = 3
    GOVERNMENT = 4
    TYPES_CHOICES = (
        (INDIVIDUAL, _("Individual")),
        (CORPORATE, _("Corporate")),
        (NON_PROFIT, _("Non-Profit")),
        (GOVERNMENT, _("Government")),
    )

    business_name = models.CharField(_("bussiness name"), max_length=255, null=True, blank=True)
    identification_no = models.CharField(_("identification number"), max_length=25, null=True, blank=True)

    email = models.EmailField(_("email address"), unique=True)

    type = models.SmallIntegerField(_("type"), choices=TYPES_CHOICES, blank=False, null=False)
    phone_number = models.CharField(_("phone number"), max_length=13, null=True, blank=True)
    address = models.CharField(_("address"), max_length=255, blank=True, null=True)
    details = models.JSONField(_("details"), null=True, blank=True)
    description = models.CharField(
        _("general user description"),
        default="",
        blank=True,
        null=False,
        max_length=500,
    )

    is_validated = models.BooleanField(default=False)

    county = models.CharField(
        _("county coverage"), max_length=2, choices=settings.COUNTY_CHOICES, blank=True, null=True
    )

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        if self.type == self.INDIVIDUAL:
            name = self.get_full_name()
        else:
            name = self.business_name
        return name if name else "-"

    def save(self, *args, **kwargs):
        self.is_staff = True  # needed to be able to log in to admin
        self.username = self.email

        if not self.first_name and not self.last_name:
            self.first_name = self.business_name
            self.last_name = self.TYPES_CHOICES[self.type - 1][1]

        super(CustomUser, self).save(*args, **kwargs)
        # all new users are added by default in the users group
        self.groups.add(Group.objects.get(name=USERS_GROUP))

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def is_regular_user(self):
        return self.groups.filter(name=USERS_GROUP).exists() and not (
            self.is_cjcci_user() or self.is_cncci_user() or self.is_superuser
        )

    def is_cjcci_user(self):
        return self.groups.filter(name=CJCCI_GROUP).exists() and not (self.is_cncci_user() or self.is_superuser)

    def is_cncci_user(self):
        return self.groups.filter(name=CNCCI_GROUP).exists() and not self.is_superuser

    def user_type(self):
        if self.is_superuser:
            return _("Admin")

        if self.is_cncci_user():
            return _(CNCCI_GROUP)

        if self.is_cjcci_user():
            return _(CJCCI_GROUP)

        if self.is_regular_user():
            return _(USERS_GROUP)

        return _("NO GROUP ASSIGNED")

    user_type.short_description = _("User Type")
