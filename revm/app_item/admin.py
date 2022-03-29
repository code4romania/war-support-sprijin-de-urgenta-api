from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from app_item import models
from revm_site.utils.admin import (
    CommonRequestInline,
    CommonOfferInline,
    CommonResourceMultipleCountyAdmin,
    CommonResourceSingleCountyAdmin,
    CountyFilter,
)


def deactivate_offers(_, request, queryset):
    if request.user.is_superuser or request.user.is_cjcci_user:
        queryset.update(status="D")

    queryset.filter(donor=request.user).update(status="D")


deactivate_offers.short_description = _("Deactivate selected offers")


class ItemOfferInline(CommonOfferInline):
    model = models.ResourceRequest


class ItemRequestInline(CommonRequestInline):
    model = models.ResourceRequest


@admin.register(models.Category)
class AdminCategory(ImportExportModelAdmin):
    list_display = ("name", "description")
    list_display_links = ("name",)
    search_fields = ("name",)

    ordering = ("pk",)

    view_on_site = False


@admin.register(models.TextileCategory)
class AdminTextileCategory(ImportExportModelAdmin):
    list_display = ("name", "description")
    list_display_links = ("name",)
    search_fields = ("name",)

    ordering = ("pk",)

    view_on_site = False


@admin.register(models.ItemOffer)
class AdminItemOffer(CommonResourceMultipleCountyAdmin):
    list_display = ("category", "name", "quantity", "stock", "unit_type", "county_coverage", "town", "get_status")
    list_display_links = ("category", "name")
    search_fields = ("name",)
    list_filter = (CountyFilter, "category", "unit_type", "textile_category", "textile_size", "status")
    readonly_fields = ("added_on", "stock", "person_phone_number")

    actions = (deactivate_offers,)

    ordering = ("pk",)

    view_on_site = False

    change_form_template = "admin/item_offer_admin.html"

    fieldsets = (
        (
            "",
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
            _("Product details"),
            {
                "fields": (
                    "textile_category",
                    "textile_size",
                    "other_textiles",
                    "name",
                    "quantity",
                    "packaging_type",
                    "unit_type",
                    "expiration_date",
                    "tent_capacity",
                    "stock",
                ),
                "classes": ("detalii-produs",),
            },
        ),
        (
            _("Offer status"),
            {
                "fields": (
                    "status",
                    "added_on",
                ),
            },
        ),
        (
            _("Location details"),
            {
                "fields": (
                    "has_transportation",
                    "county_coverage",
                    "town",
                )
            },
        ),
    )

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.requests_model = models.ItemRequest
        self.current_admin_inline = ItemOfferInline


@admin.register(models.ItemRequest)
class AdminItemRequest(CommonResourceSingleCountyAdmin):
    list_display = ("category", "name", "quantity", "stock", "unit_type", "county_coverage", "town", "get_status")
    list_display_links = ("category", "name")
    search_fields = ("name",)
    readonly_fields = ("added_on", "stock", "person_phone_number")

    list_filter = (CountyFilter, "category", "status")

    ordering = ("pk",)

    view_on_site = False

    change_form_template = "admin/item_offer_admin.html"

    fieldsets = (
        (
            "",
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
            _("Product details"),
            {
                "fields": (
                    "textile_category",
                    "textile_size",
                    "other_textiles",
                    "name",
                    "quantity",
                    "packaging_type",
                    "unit_type",
                    "tent_capacity",
                    "stock",
                ),
                "classes": ("detalii-produs",),
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
        (
            _("Where it is needed"),
            {
                "fields": (
                    "county_coverage",
                    "town",
                )
            },
        ),
    )

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.requests_model = models.ItemRequest
        self.current_admin_inline = ItemRequestInline
