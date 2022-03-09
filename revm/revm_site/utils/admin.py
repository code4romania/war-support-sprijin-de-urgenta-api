from django.conf import settings
from django.contrib import admin, messages
from django.db.models import TextField
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin


class CommonPaginatedAdmin(admin.ModelAdmin):
    list_per_page = 20

class CommonResourceInline(admin.TabularInline):
    extra = 1
    show_change_link = True
    view_on_site = True

    formfield_overrides = {TextField: {"widget": Textarea(attrs={"rows": 2, "cols": 20})}}

    def has_delete_permission(self, request, obj):
        if request.user.is_cjcci_user() or request.user.is_cncci_user():
            return False
        return super().has_delete_permission(request, obj)


class CommonOfferInline(CommonResourceInline):
    verbose_name_plural = _("Allocate this resource to a request")


class CommonRequestInline(CommonResourceInline):
    verbose_name_plural = _("Allocate from the available offers")


class CommonResourceAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()

        if not request.user.is_superuser and not request.user.is_cncci_user() and request.user.is_cjcci_user():
            if request.user.county is None:
                message_str = _("You are not assigned to any county. Please contact your administrator.")
                self.message_user(request, message_str, messages.ERROR)
                return queryset.none()

            return queryset.filter(county_coverage__contains=request.user.county)

        if request.user.is_superuser or request.user.is_cjcci_user():
            return queryset

        if request.user.is_regular_user():
            return queryset.filter(donor=request.user)

        return queryset

    class Meta:
        abstract = True


class CommonResourceSingleCountyAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()

        if not request.user.is_superuser and not request.user.is_cncci_user() and request.user.is_cjcci_user():
            if request.user.county is None:
                message_str = _("You are not assigned to any county. Please contact your administrator.")
                self.message_user(request, message_str, messages.ERROR)
                return queryset.none()

            return queryset.filter(county_coverage=request.user.county)

        if request.user.is_superuser or request.user.is_cjcci_user():
            return queryset

        if request.user.is_regular_user():
            return queryset.filter(donor=request.user)

        return queryset

    class Meta:
        abstract = True


class CountyFilter(admin.SimpleListFilter):
    title = _("County")

    parameter_name = "county"

    def lookups(self, request, model_admin):
        return settings.COUNTY_CHOICES

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value():
            return queryset.filter(
                county_coverage__contains=self.value(),
            )
        return queryset
