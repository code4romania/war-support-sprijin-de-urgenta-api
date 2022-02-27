from django.contrib import admin

from donors import models


@admin.register(models.Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "contact_name", "email", "phone_number", "details")
    search_fields = ("name", "type", "contact_name", "email", "phone_number", "details")
    list_filter = ("type",)
