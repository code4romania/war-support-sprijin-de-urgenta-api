from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from app_account.models import USERS_GROUP, DSU_GROUP
from app_volunteering import models
from revm_site.admin import CommonRequestInline, CommonOfferInline
from revm_site.utils import CountyFilter


class VolunteeringOfferInline(CommonOfferInline):
    model = models.ResourceRequest


class VolunteeringRequestInline(CommonRequestInline):
    model = models.ResourceRequest


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

        if request.user.is_superuser or request.user.groups.filter(name=DSU_GROUP).exists():
            return queryset

        if request.user.groups.filter(name=USERS_GROUP).exists():
            return queryset.filter(donor=request.user)

        return queryset


@admin.register(models.VolunteeringRequest)
class AdminVolunteeringRequest(admin.ModelAdmin):
    list_display = ("id", "made_by", "type", "county_coverage", "town", "status")
    list_display_links = ("id", "made_by")
    list_filter = ["type", CountyFilter, "status"]
    search_fields = ["name"]
    readonly_fields = ["added_on"]
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

        if request.user.is_superuser or request.user.groups.filter(name=DSU_GROUP).exists():
            return queryset

        if request.user.groups.filter(name=USERS_GROUP).exists():
            return queryset.filter(made_by=request.user)

        return queryset
