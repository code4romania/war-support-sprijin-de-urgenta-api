from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class CommonInline(admin.TabularInline):
    extra = 1
    show_change_link = True
    view_on_site = True


class CommonOfferInline(CommonInline):
    verbose_name_plural = _("Allocate this resource to a request")


class CommonRequestInline(CommonInline):
    verbose_name_plural = _("Allocate from the available offers")
