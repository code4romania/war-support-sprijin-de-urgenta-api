from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from app_food_request.models import FoodRequest
from revm_site.utils.admin import CountyFilter


@admin.register(FoodRequest)
class AdminFoodRequest(ImportExportModelAdmin):
    list_display = ("ngo_name", "status", "created_on")
    list_display_links = ("ngo_name",)
    list_filter = (CountyFilter, "status", "created_on")
    search_fields = ("ngo_name",)
