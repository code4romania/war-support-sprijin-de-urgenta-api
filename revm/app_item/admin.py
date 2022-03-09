from django.contrib import admin
from django.db.models import TextField
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from app_account.models import CustomUser
from app_item import models
from revm_site.utils.admin import (
    CommonRequestInline,
    CommonOfferInline,
    CommonResourceMultipleCountyAdmin,
    CommonResourceSingleCountyAdmin,
    CountyFilter,
)

from revm_site.utils.admin import CommonPaginatedAdmin


def deactivate_offers(modeladmin, request, queryset):
    if request.user.is_superuser or request.user.is_cjcci_user():
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
class AdminItemOffer(CommonResourceMultipleCountyAdmin, CommonPaginatedAdmin):
    list_display = ("category", "name", "quantity", "stock", "unit_type", "county_coverage", "town", "status")
    list_display_links = ("category", "name", "status")
    search_fields = ("name",)
    list_filter = (CountyFilter, "category", "unit_type", "textile_category", "kids_age", "status")
    readonly_fields = ("added_on", "stock")

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_cjcci_user():
            return [f.name for f in self.model._meta.get_fields() if f.name != "status"]
        return self.readonly_fields

    actions = (deactivate_offers,)

    inlines = (ItemOfferInline,)

    ordering = ("pk",)

    view_on_site = False

    formfield_overrides = {
        TextField: {"widget": Textarea(attrs={"rows": 3, "cols": 63})},
    }

    change_form_template = "admin/item_offer_admin.html"

    fieldsets = (
        (
            "",
            {
                "fields": (
                    "donor",
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
                    "kids_age",
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_regular_user():
            if db_field.name == "donor":
                kwargs["queryset"] = CustomUser.objects.filter(pk=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.ItemRequest)
class AdminItemRequest(CommonResourceSingleCountyAdmin, CommonPaginatedAdmin):
    list_display = ("category", "name", "quantity", "stock", "unit_type", "county_coverage", "town", "status")
    list_display_links = ("category", "name", "status")
    search_fields = ("name",)
    readonly_fields = ("added_on", "stock")

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_cjcci_user():
            return [f.name for f in self.model._meta.get_fields() if f.name != "status"]
        return self.readonly_fields

    list_filter = (CountyFilter, "category", "status")

    inlines = (ItemRequestInline,)

    ordering = ("pk",)

    view_on_site = False

    formfield_overrides = {
        TextField: {"widget": Textarea(attrs={"rows": 3, "cols": 63})},
    }

    change_form_template = "admin/item_offer_admin.html"

    fieldsets = (
        (
            "",
            {
                "fields": (
                    "made_by",
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
                    "kids_age",
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_regular_user():
            if db_field.name == "made_by":
                kwargs["queryset"] = CustomUser.objects.filter(pk=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
