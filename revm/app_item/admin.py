from django.contrib import admin
from django.db.models import TextField
from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _

from app_item import models
from app_account.models import USERS_GROUP, DSU_GROUP


def deactivate_offers(modeladmin, request, queryset):
    if request.user.is_superuser or request.user.groups.filter(name=DSU_GROUP).exists():
        queryset.update(status="D")

    queryset.filter(donor=request.user).update(status="D")


deactivate_offers.short_description = _("Deactivate selected offers")


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
    list_display = ["name", "category", "quantity", "stock", "unit_type", "donor", "status"]
    list_display_links = ["name"]
    search_fields = ["name"]
    list_filter = ["county_coverage", "category", "unit_type", "textile_category", "kids_age", "status"]
    readonly_fields = ["added_on", "stock"]
    actions = [deactivate_offers]

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
            "Detalii ridicare",
            {
                "fields": (
                    "county_coverage",
                    "pickup_town",
                    "pickup_address"
                )
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()

        if request.user.is_superuser or request.user.groups.filter(name=DSU_GROUP).exists():
            return queryset

        if request.user.groups.filter(name=USERS_GROUP).exists():
            return queryset.filter(donor=request.user)

        return queryset


@admin.register(models.ItemRequest)
class AdminItemRequest(admin.ModelAdmin):
    list_display = ["name", "category", "made_by", "status"]
    list_display_links = ["name"]
    search_fields = ["name"]
    readonly_fields = ["added_on", "stock"]

    list_filter = [
        "county_coverage",
        "category",
        "status",
    ]

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
            "Detalii ridicare",
            {
                "fields": (
                    "county_coverage",
                    "town",
                )
            },
        ),
    )
