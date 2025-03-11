from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from multiselectfield import MultiSelectField


class FoodRequest(models.Model):
    PACKAGING_CHOICES = (
        ("B", _("bulk packaging")),
        ("R", _("retail packaging")),
    )

    STATUS_CHOICES = (
        (0, _("new")),
        (1, _("in progress")),
        (2, _("solved")),
        (3, _("rejected")),
    )

    SERVICES_CHOICES = (
        ("HOST", _("hosting")),
        ("FOOD", _("food")),
        ("EDU", _("educational services")),
        ("MISC", _("other services")),
    )

    ngo_name = models.CharField(
        _("NGO name"),
        max_length=255,
        blank=False,
        null=False,
        db_index=True,
        help_text=_("NGO name or local authority name"),
    )
    county_coverage = models.CharField(
        _("county"), choices=settings.COUNTY_CHOICES, max_length=3, blank=False, null=False
    )
    town = models.CharField(_("town"), max_length=100, blank=False, null=False)
    address = models.CharField(_("address"), max_length=255, blank=False, null=False)
    contact_person = models.CharField(_("contact person"), max_length=255, blank=False, null=False)
    phone_number = models.CharField(_("phone number"), max_length=32, null=False, blank=False)
    email = models.EmailField(_("email address"), blank=False, null=False)
    backup_phone_number = models.CharField(_("backup phone number"), max_length=32, default="", null=False, blank=True)
    offered_services = MultiSelectField(_("offered services"), choices=SERVICES_CHOICES, blank=True, null=True)
    other_offered_services = models.CharField(_("other offered services"), max_length=512, blank=True, null=True)

    adult_vegetarian_portions = models.PositiveSmallIntegerField(
        _("adult vegetarian portions"),
        default=0,
        null=False,
        help_text=_("Lunch and dinner cumulated number of vegetarian portions for adults"),
    )
    child_vegetarian_portions = models.PositiveSmallIntegerField(
        _("child vegetarian portions"),
        default=0,
        null=False,
        help_text=_("Lunch and dinner cumulated number of vegetarian portions for children"),
    )
    adult_meat_portions = models.PositiveSmallIntegerField(
        _("adult meat portions"),
        default=0,
        null=False,
        help_text=_("Lunch and dinner cumulated number of meat portions for adults"),
    )
    child_meat_portions = models.PositiveSmallIntegerField(
        _("child meat portions"),
        default=0,
        null=False,
        help_text=_("Lunch and dinner cumulated number of meat portions for children"),
    )
    adult_restricted_portions = models.PositiveSmallIntegerField(
        _("adult restricted portions"),
        default=0,
        null=False,
        help_text=_("Lunch and dinner cumulated number of restriction portions for adults"),
    )
    adult_restriction_notes = models.CharField(
        _("adult restriction notes"),
        max_length=255,
        default="",
        blank=True,
        null=False,
        help_text=_("Gluten, lactose, salt... restrictions"),
    )
    child_restricted_portions = models.PositiveSmallIntegerField(
        _("child restricted portions"),
        default=0,
        null=False,
        help_text=_("Lunch and dinner cumulated number of restriction portions for children"),
    )
    child_restriction_notes = models.CharField(
        _("child restriction notes"),
        max_length=255,
        default="",
        blank=True,
        null=False,
        help_text=_("Gluten, lactose, salt... restrictions"),
    )

    delivery_hours = models.CharField(_("delivery hours"), max_length=255, blank=False, null=False)
    delivery_daily_frequency = models.CharField(_("delivery daily frequency"), max_length=255, blank=False, null=False)

    preferred_packaging = models.CharField(
        _("preferred packaging"), max_length=1, default="B", blank=False, null=False, choices=PACKAGING_CHOICES
    )
    notes = models.TextField(_("notes"), default="", blank=True, null=False)

    status = models.PositiveSmallIntegerField(
        _("status"), default=0, choices=STATUS_CHOICES, blank=False, null=False, db_index=True
    )
    created_on = models.DateTimeField(
        _("created on"), blank=True, null=False, editable=False, auto_now_add=timezone.now
    )

    def __str__(self):
        return f"#{self.id} {self.ngo_name}"

    class Meta:
        verbose_name = _("NGO food request")
        verbose_name_plural = _("NGO food requests")
