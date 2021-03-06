from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from app_transport_service import models
from revm_site.utils.admin import (
    CommonRequestInline,
    CommonOfferInline,
    CommonResourceMultipleCountyAdmin,
    CountyFilter,
    CommonResourceToFromCountyAdmin,
)


class TransportOfferInline(CommonOfferInline):
    model = models.ResourceRequest


class TransportRequestInline(CommonRequestInline):
    model = models.ResourceRequest


@admin.register(models.Category)
class AdminCategoryRequest(ImportExportModelAdmin):
    list_display = ("name", "description")
    list_display_links = ("name",)
    search_fields = ("name",)

    ordering = ("pk",)

    view_on_site = False


@admin.register(models.TransportServiceOffer)
class AdminTransportServiceOffer(CommonResourceMultipleCountyAdmin):
    list_display = ("category", "capacitate", "type", "availability", "county_coverage", "get_status")
    list_display_links = ("category",)
    list_filter = ("category", "status", "availability", CountyFilter)
    search_fields = ()
    readonly_fields = ("added_on", "person_phone_number")

    ordering = ("pk",)

    view_on_site = False
    change_form_template = "admin/transport_offer_admin.html"

    fieldsets = (
        (
            _("Offer details"),
            {
                "fields": (
                    "donor",
                    "person_phone_number",
                    "category",
                    "description",
                )
            },
        ),
        (
            _("Transport details"),
            {
                "fields": ("weight_capacity", "weight_unit", "has_refrigeration"),
                "classes": ("transport-marfa",),
            },
        ),
        (
            _("Transport details"),
            {
                "fields": ("available_seats", "has_disabled_access", "pets_allowed"),
                "classes": ("transport-persoane",),
            },
        ),
        (
            _("Availability"),
            {
                "fields": (
                    "type",
                    "county_coverage",
                    "availability",
                    "availability_interval_from",
                    "availability_interval_to",
                )
            },
        ),
        (
            _("Driver details"),
            {"fields": ("driver_name", "driver_contact", "driver_id", "car_registration_number")},
        ),
        (
            _("Offer status"),
            {
                "fields": ("status", "added_on"),
            },
        ),
    )

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.requests_model = models.TransportServiceRequest
        self.current_admin_inline = TransportOfferInline

    def capacitate(self, obj):
        if obj.available_seats:
            return f"{obj.available_seats} locuri"
        return f"{obj.weight_capacity} {obj.weight_unit}"


@admin.register(models.TransportServiceRequest)
class AdminTransportServiceRequest(CommonResourceToFromCountyAdmin):
    list_display = ("category", "capacitate", "de_la", "la", "get_status")
    list_display_links = ("category",)
    search_fields = ()
    readonly_fields = ("added_on", "person_phone_number")

    ordering = ("pk",)
    view_on_site = False

    change_form_template = "admin/transport_offer_admin.html"

    fieldsets = (
        (
            _("Request details"),
            {
                "fields": (
                    "made_by",
                    "person_phone_number",
                    "category",
                    "description",
                )
            },
        ),
        (
            _("Transport details"),
            {
                "fields": (
                    "weight_capacity",
                    "weight_unit",
                    "has_refrigeration",
                ),
                "classes": ("transport-marfa",),
            },
        ),
        (
            _("Transport details"),
            {
                "fields": (
                    "available_seats",
                    "has_disabled_access",
                    "pets_allowed",
                ),
                "classes": ("transport-persoane",),
            },
        ),
        (
            _("Location details"),
            {
                "fields": (
                    "from_county",
                    "from_city",
                    "to_county",
                    "to_city",
                )
            },
        ),
        (
            _("Request status"),
            {
                "fields": (
                    "status",
                    "added_on",
                ),
            },
        ),
    )

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.requests_model = models.TransportServiceRequest
        self.current_admin_inline = TransportRequestInline

    def capacitate(self, obj):
        if obj.available_seats:
            return f"{obj.available_seats} locuri"
        return f"{obj.weight_capacity} {obj.weight_unit}"

    def de_la(self, obj):
        return f"{obj.from_city} ({obj.from_county})"

    def la(self, obj):
        return f"{obj.to_city} ({obj.to_county})"
