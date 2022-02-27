from django.contrib import admin

from available_resources import models


@admin.register(models.FoodProductsResource)
class ResourceAdmin(admin.ModelAdmin):
    list_filter = (
        "subcategory",
        "county_coverage",
    )
    list_display = (
        "name",
        "subcategory",
        "county_coverage",
    )

    search_fields = ("name",)


@admin.register(models.GoodsTransportService)
class GoodsTransportServiceAdmin(admin.ModelAdmin):
    list_filter = ("county_coverage", "currently_in_use")
    list_display = ("name", "usable_weight", "has_refrigeration", "county_coverage", "reuses_left", "currently_in_use")


@admin.register(models.PeopleTransportService)
class PeopleTransportServiceAdmin(admin.ModelAdmin):
    list_filter = ("county_coverage", "currently_in_use", "total_passengers")
    list_display = ("name", "total_passengers", "has_disability_access", "has_pet_accommodation")
