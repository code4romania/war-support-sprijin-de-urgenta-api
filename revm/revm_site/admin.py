from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin


class CommonInline(admin.TabularInline):
    extra = 1
    show_change_link = True
    view_on_site = True


class CommonOfferInline(CommonInline):
    verbose_name_plural = _("Allocate this resource to a request")


class CommonRequestInline(CommonInline):
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
