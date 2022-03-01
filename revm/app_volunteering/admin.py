from django.contrib import admin
from app_volunteering import models


class OtherResourceRequestInline(admin.TabularInline):
    model = models.ResourceRequest
    extra = 0
    show_change_link = True
    view_on_site = True


@admin.register(models.Type)
class AdminOtherRequest(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    list_display_links = ("id", "name")
    search_fields = ["name"]

    ordering = ("pk",)

    view_on_site = False


@admin.register(models.VolunteeringOffer)
class AdminVolunteeringOffer(admin.ModelAdmin):
    list_display = ("id", "donor", "type")
    list_display_links = ("id", "donor")
    search_fields = ["name"]

    inlines = (OtherResourceRequestInline,)

    ordering = ("pk",)

    view_on_site = False


@admin.register(models.VolunteeringRequest)
class AdminVolunteeringRequest(admin.ModelAdmin):
    list_display = ("id", "made_by", "type")
    list_display_links = ("id", "made_by")
    search_fields = ["name"]

    inlines = (OtherResourceRequestInline,)

    ordering = ("pk",)

    view_on_site = False
