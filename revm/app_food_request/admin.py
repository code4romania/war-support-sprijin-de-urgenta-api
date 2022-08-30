from django.contrib import admin

from revm_site.utils.admin import CountyFilter
from app_food_request.models import FoodRequest


@admin.register(FoodRequest)
class AdminFoodRequest(admin.ModelAdmin):
    list_display = ("ngo_name", "status", "created_on")
    list_display_links = ("ngo_name",)
    list_filter = (CountyFilter, "status", "created_on")
    search_fields = ("ngo_name",)
