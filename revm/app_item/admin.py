from django.db.models import TextField
from django.forms import TextInput, Textarea
from django.contrib import admin

from app_item import models


class OtherResourceRequestInline(admin.TabularInline):
    model = models.ResourceRequest
    extra = 1
    show_change_link = True
    view_on_site = True

    formfield_overrides = {
        TextField: {"widget": Textarea(attrs={"rows": 3, "cols": 40})},
    }


@admin.register(models.Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    list_display_links = ("id", "name")
    search_fields = ["name"]

    ordering = ("pk",)

    view_on_site = False

@admin.register(models.TextileCategory)
class AdminTextileCategory(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    list_display_links = ("id", "name")
    search_fields = ["name"]

    ordering = ("pk",)

    view_on_site = False


@admin.register(models.ItemOffer)
class AdminItemOffer(admin.ModelAdmin):
    list_display = ("id", "name", "category", "quantity", "stock", "unit_type", "donor", "status")
    list_display_links = ("id", "name")
    search_fields = ["name"]
    list_filter = ["county_coverage", "category", "unit_type", "textile_category", "kids_age", "status"]
    readonly_fields = ["added_on", "stock"]

    inlines = (OtherResourceRequestInline,)

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
            "Detalii produs",
            {
                "fields": (
                    "name",
                    "quantity",
                    "packaging_type",
                    "unit_type",
                    "expiration_date",
                    "textile_category",
                    "kids_age",
                    "other_textiles",
                    "tent_capacity",
                    "stock",
                ),
                "classes": ("detalii-produs", )
            },
        ),
        (
            "Detalii ridicare",
            {
                "fields": (
                    "county_coverage",
                    "pickup_town",
                )
            },
        ),
    )


@admin.register(models.ItemRequest)
class AdminItemRequest(admin.ModelAdmin):
    list_display = ("id", "name", "category", "made_by", "status")
    list_display_links = ("id", "name")
    search_fields = ["name"]
    readonly_fields = ["made_by", "added_on", "stock"]
    list_filter = ["county_coverage", "category", "status", ]

    inlines = (OtherResourceRequestInline,)

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
            "Detalii produs",
            {
                "fields": (
                    "name",
                    "quantity",
                    "packaging_type",
                    "unit_type",
                    "expiration_date",
                    "stock",
                    "textile_category",
                    "kids_age",
                    "other_textiles",
                    "tent_capacity",
                )
            },
        ),
        (
            "Detalii ridicare",
            {
                "fields": (
                    "county_coverage",
                    "pickup_town",
                )
            },
        ),
    )
