from django.contrib import admin
from app_transport_service import models


class OtherResourceRequestInline(admin.TabularInline):
    model = models.ResourceRequest
    extra = 1
    show_change_link = True
    view_on_site = True


@admin.register(models.Category)
class AdminOtherRequest(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    list_display_links = ("id", "name")
    search_fields = ["name"]

    ordering = ("pk",)

    view_on_site = False


@admin.register(models.Subcategory)
class AdminOtherRequest(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_display_links = ("id", "name")
    search_fields = ["name"]

    ordering = ("pk",)

    view_on_site = False


@admin.register(models.TransportServiceOffer)
class AdminTransportServiceOffer(admin.ModelAdmin):
    list_display = ("id", "donor", "name", "category")
    list_display_links = ("id", "name")
    search_fields = ["name"]

    inlines = (OtherResourceRequestInline,)

    ordering = ("pk",)

    view_on_site = False
    change_form_template = 'admin/transport_offer_admin.html'

    fieldsets = (
                (
                    "Detalii ofertă",
                    {
                        "fields": (
                            "donor",
                            "category",
                            "name",
                            "description",
                        )
                    },
                ),
                ("Detalii șofer", {"fields": (
                    "driver_name",
                    "driver_id",
                    "car_registration_number",

                    )}),
                ("Disponibilitate", {"fields": (
                    "type",
                    "available_from",
                    "available_until",
                    "availability",
                    "availability_interval_from",
                    "availability_interval_to",

                    "county_coverage",
                    "town",

                    )}),
                ("Detalii transport marfa", {"fields": (

                    "weight_capacity",
                    "weight_unit",
                    "volume",
                    "volume_unit",
                    "has_refrigeration",

                    ),
                    "classes": ("transport-marfa",)
                }),
                ("Detalii transport persoane", {"fields": (
                    "available_seats",
                    "has_disabled_access",
                    "pets_allowed",

                    ),
                    "classes": ("transport-persoane",)
                }),
            )


@admin.register(models.TransportServiceRequest)
class AdminTransportServiceRequest(admin.ModelAdmin):
    list_display = ("id", "made_by", "name", "category")
    list_display_links = ("id", "name")
    search_fields = ["name"]

    inlines = (OtherResourceRequestInline,)

    ordering = ("pk",)

    view_on_site = False
