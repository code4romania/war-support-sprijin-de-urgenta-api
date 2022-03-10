from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from app_volunteering import models
from revm_site.utils.admin import (
    CommonRequestInline,
    CommonOfferInline,
    CommonResourceMultipleCountyAdmin,
    CountyFilter,
)


class VolunteeringOfferInline(CommonOfferInline):
    model = models.ResourceRequest


class VolunteeringRequestInline(CommonRequestInline):
    model = models.ResourceRequest


@admin.register(models.Type)
class AdminTypeRequest(ImportExportModelAdmin):
    list_display = ("name", "description")
    list_display_links = ("name",)
    search_fields = ("name",)

    ordering = ("pk",)

    view_on_site = False


@admin.register(models.VolunteeringOffer)
class AdminVolunteeringOffer(CommonResourceMultipleCountyAdmin):
    list_display = ("donor", "type", "county_coverage", "town", "available_until", "get_status")
    list_display_links = ("donor",)
    list_filter = ("type", CountyFilter, "status")
    search_fields = ("name",)
    readonly_fields = ("added_on",)

    ordering = ("pk",)

    view_on_site = False

    fieldsets = (
        (
            _("Offer details"),
            {
                "fields": (
                    "donor",
                    "type",
                    "name",
                    "available_until",
                    "has_transportation",
                    "county_coverage",
                    "town",
                    "added_on",
                    "status",
                )
            },
        ),
    )

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.current_admin_inline = VolunteeringOfferInline


@admin.register(models.VolunteeringRequest)
class AdminVolunteeringRequest(CommonResourceMultipleCountyAdmin):
    list_display = ("made_by", "type", "county_coverage", "town", "get_status")
    list_display_links = ("made_by",)
    list_filter = ("type", CountyFilter, "status")
    search_fields = ("name",)
    readonly_fields = ("added_on",)

    ordering = ("pk",)

    view_on_site = False

    fieldsets = (
        (
            _("Request details"),
            {"fields": ("made_by", "type", "county_coverage", "town", "added_on", "status")},
        ),
    )

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.current_admin_inline = VolunteeringRequestInline
