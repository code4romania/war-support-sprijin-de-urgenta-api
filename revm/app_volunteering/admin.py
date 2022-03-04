from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from app_account.models import CustomUser
from app_volunteering import models
from revm_site.admin import CommonRequestInline, CommonOfferInline
from revm_site.utils import CountyFilter


class VolunteeringOfferInline(CommonOfferInline):
    model = models.ResourceRequest

    def has_change_permission(self, request, obj):
        if request.user.is_dsu_user():
            return False
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request, obj):
        if request.user.is_dsu_user():
            return False
        return super().has_add_permission(request, obj)

    def has_delete_permission(self, request, obj):
        if request.user.is_dsu_user():
            return False
        return super().has_delete_permission(request, obj)

class VolunteeringRequestInline(CommonRequestInline):
    model = models.ResourceRequest

    def has_change_permission(self, request, obj):
        if request.user.is_dsu_user():
            return False
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request, obj):
        if request.user.is_dsu_user():
            return False
        return super().has_add_permission(request, obj)

    def has_delete_permission(self, request, obj):
        if request.user.is_dsu_user():
            return False
        return super().has_delete_permission(request, obj)

@admin.register(models.Type)
class AdminTypeRequest(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    list_display_links = ("id", "name")
    search_fields = ["name"]

    ordering = ("pk",)

    view_on_site = False


@admin.register(models.VolunteeringOffer)
class AdminVolunteeringOffer(admin.ModelAdmin):
    list_display = ("id", "donor", "type", "county_coverage", "town", "available_until", "status")
    list_display_links = ("id", "donor")
    list_filter = ["type", CountyFilter, "status"]
    search_fields = ["name"]
    readonly_fields = ["added_on"]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_dsu_user():
            return [f.name for f in self.model._meta.get_fields() if f.name != "status"]
        return self.readonly_fields

    inlines = (VolunteeringOfferInline,)

    ordering = ("pk",)

    view_on_site = False

    fieldsets = (
        (
            _("Offer details"),
            {
                "fields": (
                    "donor",
                    "type",
                    "available_until",
                    "county_coverage",
                    "town",
                    "added_on",
                    "status",
                )
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()

        if request.user.is_superuser or request.user.is_dsu_user():
            return queryset

        if request.user.is_regular_user():
            return queryset.filter(donor=request.user)

        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_regular_user():
            if db_field.name == "donor":
                kwargs["queryset"] = CustomUser.objects.filter(pk=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.VolunteeringRequest)
class AdminVolunteeringRequest(admin.ModelAdmin):
    list_display = ("id", "made_by", "type", "county_coverage", "town", "status")
    list_display_links = ("id", "made_by")
    list_filter = ["type", CountyFilter, "status"]
    search_fields = ["name"]
    readonly_fields = ["added_on"]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_dsu_user():
            return [f.name for f in self.model._meta.get_fields() if f.name != "status"]
        return self.readonly_fields

    inlines = (VolunteeringRequestInline,)

    ordering = ("pk",)

    view_on_site = False

    fieldsets = (
        (
            _("Request details"),
            {
                "fields": (
                    "made_by",
                    "type",
                    "county_coverage",
                    "town",
                    "added_on",
                    "status",
                )
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()

        if request.user.is_superuser or request.user.is_dsu_user():
            return queryset

        if request.user.is_regular_user():
            return queryset.filter(made_by=request.user)

        return queryset
