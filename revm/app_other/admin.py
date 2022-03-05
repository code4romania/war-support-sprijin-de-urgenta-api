from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from app_account.models import CustomUser
from app_other import models
from revm_site.admin import CommonRequestInline, CommonOfferInline
from revm_site.utils import CountyFilter


class OtherOfferInline(CommonOfferInline):
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


class OtherRequestInline(CommonRequestInline):
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


@admin.register(models.Category)
class AdminCategoryRequest(ImportExportModelAdmin):
    list_display = ("id", "name", "description")
    list_display_links = ("id", "name")
    search_fields = ["name"]

    ordering = ("pk",)

    view_on_site = False


@admin.register(models.OtherOffer)
class AdminOtherOffer(ImportExportModelAdmin):
    list_display = (
        "id",
        "category",
        "name",
        "available_until",
        "county_coverage",
        "town",
        "status",
    )
    list_display_links = ("id", "name")
    search_fields = ["name"]
    readonly_fields = ["added_on"]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_dsu_user():
            return [f.name for f in self.model._meta.get_fields() if f.name != "status"]
        return self.readonly_fields

    list_filter = ("category", "status", CountyFilter)
    inlines = (OtherOfferInline,)

    ordering = ("pk",)

    view_on_site = False

    fieldsets = (
        (
            _("Offer details"),
            {
                "fields": (
                    "donor",
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()

        if not request.user.is_superuser and request.user.is_dsu_user():
            return queryset.filter(county_coverage__contains=request.user.county)

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


@admin.register(models.OtherRequest)
class AdminOtherRequest(ImportExportModelAdmin):
    list_display = ("id", "category", "name", "county_coverage", "town", "status")
    list_display_links = ("id", "name")
    search_fields = ["name"]
    readonly_fields = ["added_on"]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_dsu_user():
            return [f.name for f in self.model._meta.get_fields() if f.name != "status"]
        return self.readonly_fields

    list_filter = ("category", "status", CountyFilter)

    inlines = (OtherRequestInline,)

    ordering = ("pk",)

    view_on_site = False

    fieldsets = (
        (
            _("Request details"),
            {
                "fields": (
                    "made_by",
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()

        if not request.user.is_superuser and request.user.is_dsu_user():
            return queryset.filter(county_coverage__contains=request.user.county)

        if request.user.is_superuser or request.user.is_dsu_user():
            return queryset

        if request.user.is_regular_user():
            return queryset.filter(made_by=request.user)

        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_regular_user():
            if db_field.name == "made_by":
                kwargs["queryset"] = CustomUser.objects.filter(pk=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
