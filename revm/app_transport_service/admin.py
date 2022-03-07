from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from app_account.models import CustomUser
from app_transport_service import models
from revm_site.utils.admin import CommonRequestInline, CommonOfferInline, CommonResourceAdmin, CountyFilter


class TransportOfferInline(CommonOfferInline):
    model = models.ResourceRequest

    def has_change_permission(self, request, obj):
        if request.user.is_cjcci_user():
            return False
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request, obj):
        if request.user.is_cjcci_user():
            return False
        return super().has_add_permission(request, obj)

    def has_delete_permission(self, request, obj):
        if request.user.is_cjcci_user():
            return False
        return super().has_delete_permission(request, obj)


class TransportRequestInline(CommonRequestInline):
    model = models.ResourceRequest

    def has_change_permission(self, request, obj):
        if request.user.is_cjcci_user():
            return False
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request, obj):
        if request.user.is_cjcci_user():
            return False
        return super().has_add_permission(request, obj)

    def has_delete_permission(self, request, obj):
        if request.user.is_cjcci_user():
            return False
        return super().has_delete_permission(request, obj)


@admin.register(models.Category)
class AdminCategoryRequest(ImportExportModelAdmin):
    list_display = ("id", "name", "description")
    list_display_links = ("id", "name")
    search_fields = ["name"]

    ordering = ("pk",)

    view_on_site = False


@admin.register(models.TransportServiceOffer)
class AdminTransportServiceOffer(CommonResourceAdmin):
    list_display = ("id", "category", "capacitate", "type", "availability", "county_coverage", "status")
    list_display_links = ("id", "category")
    list_filter = ("category", "status", "availability", CountyFilter)
    search_fields = []
    readonly_fields = ("added_on",)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_cjcci_user():
            return [f.name for f in self.model._meta.get_fields() if f.name != "status"]
        return self.readonly_fields

    inlines = (TransportOfferInline,)

    ordering = ("pk",)

    view_on_site = False
    change_form_template = "admin/transport_offer_admin.html"

    def capacitate(self, obj):
        if obj.available_seats:
            return f"{obj.available_seats} locuri"
        return f"{obj.weight_capacity} {obj.weight_unit}"

    fieldsets = (
        (
            _("Offer details"),
            {
                "fields": (
                    "donor",
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
            {
                "fields": (
                    "driver_name",
                    "driver_contact",
                    "driver_id",
                    "car_registration_number",
                )
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
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_regular_user():
            if db_field.name == "donor":
                kwargs["queryset"] = CustomUser.objects.filter(pk=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.TransportServiceRequest)
class AdminTransportServiceRequest(CommonResourceAdmin):
    list_display = ("id", "category", "capacitate", "de_la", "la", "status")
    list_display_links = ("id", "category")
    search_fields = []
    readonly_fields = ["added_on"]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_cjcci_user():
            return [f.name for f in self.model._meta.get_fields() if f.name != "status"]
        return self.readonly_fields

    inlines = (TransportRequestInline,)

    ordering = ("pk",)
    view_on_site = False

    change_form_template = "admin/transport_offer_admin.html"

    def capacitate(self, obj):
        if obj.available_seats:
            return f"{obj.available_seats} locuri"
        return f"{obj.weight_capacity} {obj.weight_unit}"

    def de_la(self, obj):
        return f"{obj.from_city} ({obj.from_county})"

    def la(self, obj):
        return f"{obj.to_city} ({obj.to_county})"

    fieldsets = (
        (
            _("Request details"),
            {
                "fields": (
                    "made_by",
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_regular_user():
            if db_field.name == "made_by":
                kwargs["queryset"] = CustomUser.objects.filter(pk=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
