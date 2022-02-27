from django.contrib import admin

from available_resources import models


@admin.register(models.ResourceSubcategory)
class ResourceSubcategoryAdmin(admin.ModelAdmin):
    list_filter = ("name", "category",)
    list_display = ("name", "category", "description")

    search_fields = ("name",)

    ordering = ('name', )


@admin.register(models.ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    list_display = ("name", "description")

    search_fields = ("name",)

    ordering = ('name', )


@admin.register(models.GoodsTransportService)
class GoodsTransportServiceAdmin(admin.ModelAdmin):
    list_filter = ("county_coverage", "currently_in_use")
    list_display = ("name", "category", "usable_weight", "has_refrigeration", "county_coverage", "reuses_left",
                    "currently_in_use")

    # custom `category` field added to the list view in Admin Panel
    def category(self, instance):
        return instance.subcategory.category.name

    category.short_description = 'Category'


@admin.register(models.PeopleTransportService)
class PeopleTransportServiceAdmin(admin.ModelAdmin):
    list_filter = ("county_coverage", "currently_in_use", "total_passengers")
    list_display = ("name", "category", "total_passengers", "has_disability_access", "has_pet_accommodation")

    # custom `category` field added to the list view in Admin Panel
    def category(self, instance):
        return instance.subcategory.category.name

    category.short_description = 'Category'


@admin.register(models.FoodProductsResource)
class FoodProductsResourceAdmin(admin.ModelAdmin):
    list_filter = ("pickup_town",)
    list_display = ("name", "category", "total_units", "unit_type")

    # custom `category` field added to the list view in Admin Panel
    def category(self, instance):
        return instance.subcategory.category.name

    category.short_description = 'Category'
