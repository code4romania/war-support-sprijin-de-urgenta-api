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
        TextField: {"widget": Textarea(attrs={"rows":3, "cols":40})},
    }

@admin.register(models.Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    list_display_links = ("id", "name")
    search_fields = ["name"]

    ordering = ("pk",)

    view_on_site = False


@admin.register(models.Subcategory)
class AdminSubcategory(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_display_links = ("id", "name")
    search_fields = ["name"]

    ordering = ("pk",)

    view_on_site = False


@admin.register(models.ItemOffer)
class AdminItemOffer(admin.ModelAdmin):
    list_display = (
        "id", "name", "subcategory", "total_units",
        "units_left", "unit_type", "donor",
        "status"
        )
    list_display_links = ("id", "name")
    search_fields = ["name"]
    list_filter = ["county_coverage", "subcategory", "unit_type"]
    readonly_fields = ["added_on"]

    inlines = (OtherResourceRequestInline,)

    ordering = ("pk",)

    view_on_site = False

    formfield_overrides = {
        TextField: {"widget": Textarea(attrs={"rows":3, "cols":63})},
    }

@admin.register(models.ItemRequest)
class AdminItemRequest(admin.ModelAdmin):
    list_display = (
        "id", "name", "subcategory", "made_by",
        "status"
        )
    list_display_links = ("id", "name")
    search_fields = ["name"]
    readonly_fields = ["added_on"]
    list_filter = ["county_coverage", "subcategory", "status"]

    inlines = (OtherResourceRequestInline,)

    ordering = ("pk",)

    view_on_site = False

    formfield_overrides = {
        TextField: {"widget": Textarea(attrs={"rows":3, "cols":63})},
    }