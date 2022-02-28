from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from available_resources import models


@admin.register(models.ResourceCategory)
class ResourceCategoryAdmin(ImportExportModelAdmin):
    list_filter = ("name",)
    list_display = ("name", "description")

    search_fields = ("name",)

    ordering = ("name",)


@admin.register(models.ResourceSubcategory)
class ResourceSubcategoryAdmin(ImportExportModelAdmin):
    list_filter = ("name", "category")
    list_display = ("name", "category", "description")

    search_fields = ("name",)

    ordering = ("name",)


@admin.register(models.GoodsTransportService)
class GoodsTransportServiceAdmin(ImportExportModelAdmin):
    list_filter = ("county_coverage", "currently_in_use")
    list_display = (
        "name",
        "category",
        "subcategory",
        "usable_weight",
        "has_refrigeration",
        "county_coverage",
        "reuses_left",
        "currently_in_use",
    )

    # custom `category` field added to the list view in Admin Panel
    def category(self, instance):
        return instance.subcategory.category.name

    category.short_description = "Category"


@admin.register(models.PeopleTransportService)
class PeopleTransportServiceAdmin(ImportExportModelAdmin):
    list_filter = ("county_coverage", "currently_in_use", "total_passengers")
    list_display = ("name", "category", "subcategory", "total_passengers", "has_disability_access",
                    "has_pet_accommodation")

    # custom `category` field added to the list view in Admin Panel
    def category(self, instance):
        return instance.subcategory.category.name

    category.short_description = "Category"


@admin.register(models.ProductsResource)
class ProductsResourceAdmin(ImportExportModelAdmin):
    list_filter = ("pickup_town",)
    list_display = ("name", "category", "subcategory", "total_units", "unit_type")

    # custom `category` field added to the list view in Admin Panel
    def category(self, instance):
        return instance.subcategory.category.name

    category.short_description = "Category"


@admin.register(models.VolunteeringResource)
class VolunteeringResourceAdmin(ImportExportModelAdmin):
    list_filter = ("type", "county_coverage")
    list_display = ("name", "county_coverage", "type")


@admin.register(models.OtherResource)
class OtherResourceAdmin(ImportExportModelAdmin):
    list_filter = ("donor",)
    list_display = ("donor", "description")
