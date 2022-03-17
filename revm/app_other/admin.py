from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from app_other import models
from revm_site.utils.admin.admin_resource import (
    CommonRequestInline,
    CommonOfferInline,
    CommonResourceMultipleCountyAdmin,
    CountyFilter,
)
from revm_site.utils.admin.admin_category import CommonCategoryAdmin


@admin.register(models.Category)
class AdminCategory(CommonCategoryAdmin):
    ...


class OtherOfferInline(CommonOfferInline):
    model = models.ResourceRequest


class OtherRequestInline(CommonRequestInline):
    model = models.ResourceRequest


@admin.register(models.OtherOffer)
class AdminOtherOffer(CommonResourceMultipleCountyAdmin):
    list_display = ("category", "name", "available_until", "county_coverage", "town", "get_status")
    list_display_links = ("name",)
    search_fields = ("name",)
    readonly_fields = ("added_on", "person_phone_number")

    list_filter = ("category", "status", CountyFilter)

    ordering = ("pk",)

    view_on_site = False

    fieldsets = (
        (
            _("Offer details"),
            {
                "fields": (
                    "donor",
                    "person_phone_number",
                    "category",
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
        self.requests_model = models.OtherRequest
        self.current_admin_inline = OtherOfferInline


@admin.register(models.OtherRequest)
class AdminOtherRequest(CommonResourceMultipleCountyAdmin):
    list_display = ("category", "name", "county_coverage", "town", "get_status")
    list_display_links = ("name",)
    search_fields = ("name",)
    readonly_fields = ("added_on", "person_phone_number")

    list_filter = ("category", "status", CountyFilter)

    ordering = ("pk",)

    view_on_site = False

    fieldsets = (
        (
            _("Request details"),
            {
                "fields": (
                    "made_by",
                    "person_phone_number",
                    "category",
                    "name",
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
        self.requests_model = models.OtherRequest
        self.current_admin_inline = OtherRequestInline
