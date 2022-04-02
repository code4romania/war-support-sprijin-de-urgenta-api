from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from app_volunteering import models
from revm_site.utils.admin.admin_category import CommonCategoryAdmin
from revm_site.utils.admin.admin_resource import (
    CommonRequestInline,
    CommonOfferInline,
    CommonResourceMultipleCountyAdmin,
    CountyFilter,
)


class VolunteeringOfferInline(CommonOfferInline):
    model = models.ResourceRequest


class VolunteeringRequestInline(CommonRequestInline):
    model = models.ResourceRequest


@admin.register(models.VolunteeringOffer)
class AdminVolunteeringOffer(CommonResourceMultipleCountyAdmin):
    list_display = ("donor", "type", "county_coverage", "town", "available_until", "get_status")
    list_display_links = ("donor",)
    list_filter = ("type", CountyFilter, "status")
    search_fields = ("name",)
    readonly_fields = ("added_on", "person_phone_number")

    ordering = ("pk",)

    view_on_site = False

    fieldsets = (
        (
            _("Offer details"),
            {
                "fields": (
                    "donor",
                    "person_phone_number",
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
        self.requests_model = models.VolunteeringRequest
        self.current_admin_inline = VolunteeringOfferInline


@admin.register(models.VolunteeringRequest)
class AdminVolunteeringRequest(CommonResourceMultipleCountyAdmin):
    list_display = ("made_by", "type", "county_coverage", "town", "get_status")
    list_display_links = ("made_by",)
    list_filter = ("type", CountyFilter, "status")
    search_fields = ("name",)
    readonly_fields = ("added_on", "person_phone_number")

    ordering = ("pk",)

    view_on_site = False

    fieldsets = (
        (
            _("Request details"),
            {"fields": ("made_by", "person_phone_number", "type", "county_coverage", "town", "added_on", "status")},
        ),
    )

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.requests_model = models.VolunteeringRequest
        self.current_admin_inline = VolunteeringRequestInline


admin.site.register(models.Category, CommonCategoryAdmin)
