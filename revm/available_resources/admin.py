from django.contrib import admin

from available_resources import models


@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_filter = ("category", "donor_county",)
    list_display = ("name", "category", "donor_county",)

    search_fields = ("name",)
