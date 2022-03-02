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


@admin.register(models.TransportServiceOffer)
class AdminTransportServiceOffer(admin.ModelAdmin):
    list_display = ("id", "__str__", "donor", "category")
    list_display_links = ("id", "__str__")
    search_fields = []
    readonly_fields = ('added_on',)
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
                            "description",
                        )
                    },
                ),
                ("Detalii transport marfa", {"fields": (
                    "weight_capacity",
                    "weight_unit",
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
                ("Disponibilitate", {"fields": (
                    "type",
                    "county_coverage",
                    "availability",
                    "availability_interval_from",
                    "availability_interval_to",
                )}),
                ("Detalii șofer", {"fields": (
                    "driver_name",
                    "driver_id",
                    "car_registration_number",
                )}),
                ("Detalii ofertă", {"fields": (
                    "status",
                    "added_on",
                    ),
                }),
            )


@admin.register(models.TransportServiceRequest)
class AdminTransportServiceRequest(admin.ModelAdmin):
    list_display = ("id", "__str__", "made_by", "category")
    list_display_links = ("id", "__str__")
    search_fields = []
    readonly_fields = ["added_on"]
    inlines = (OtherResourceRequestInline,)

    ordering = ("pk",)
    view_on_site = False

    change_form_template = 'admin/transport_offer_admin.html'

    fieldsets = (
                (
                "Detalii ofertă",
                    {
                        "fields": (
                            "made_by",
                            "category",
                            "description",
                        )
                    },
                ),
                ("Detalii transport marfa", {"fields": (
                    "weight_capacity",
                    "weight_unit",
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
                ("Detalii transport", {"fields": (
                    "from_county",
                    "from_city",
                    "to_county",
                    "to_city",
                )}),
                ("Detalii ofertă", {"fields": (
                    "status",
                    "added_on",
                    ),
                }),
            )