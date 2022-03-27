from django.conf import settings
from django.utils.translation import gettext_lazy as _


def _set_resource_status(queryset, request, status):
    if request.user.is_superuser or request.user.is_cjcci_user():
        queryset.update(status=status)
    queryset.filter(donor=request.user).update(status=status)


def set_resources_status_deactivated(_, request, queryset):
    status = settings.ITEM_STATUS_DEACTIVATED
    _set_resource_status(queryset, request, status)


def set_resources_status_completed(_, request, queryset):
    status = settings.ITEM_STATUS_COMPLETE
    _set_resource_status(queryset, request, status)


set_resources_status_deactivated.short_description = _("Mark selected resources as deactivated")
set_resources_status_completed.short_description = _("Mark selected resources as completed")
