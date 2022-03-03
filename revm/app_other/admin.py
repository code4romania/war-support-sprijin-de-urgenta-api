from django.contrib import admin
from app_account.models import USERS_GROUP, DSU_GROUP

from app_other import models
from revm_site.utils import CountyFilter

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


@admin.register(models.OtherOffer)
class AdminOtherOffer(admin.ModelAdmin):
    list_display = ("id","category", "name", "available_until", "county_coverage", "town", "status")
    list_display_links = ("id", "name")
    search_fields = ["name"]
    readonly_fields = ["added_on"]
    list_filter = ("category",  "status", CountyFilter)
    inlines = (OtherResourceRequestInline,)

    ordering = ("pk",)

    view_on_site = False


    fieldsets = (
        (
            "Detalii ofertă",
            {
                "fields": (
                    "donor",
                    "category",
                    "name",
                    "available_until",
                    "county_coverage",
                    "town",
                    "added_on",
                    "status",
                    
                )
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()

        if (
            request.user.is_superuser
            or request.user.groups.filter(name=DSU_GROUP).exists()
        ):
            return queryset

        if request.user.groups.filter(name=USERS_GROUP).exists():
            return queryset.filter(donor=request.user)

        return queryset

@admin.register(models.OtherRequest)
class AdminOtherRequest(admin.ModelAdmin):
    list_display = ("id","category", "name", "county_coverage", "town", "status")
    list_display_links = ("id", "name")
    search_fields = ["name"]
    readonly_fields = ["added_on"]
    list_filter = ("category",  "status", CountyFilter)

    inlines = (OtherResourceRequestInline,)

    ordering = ("pk",)

    view_on_site = False



    fieldsets = (
        (
            "Detalii ofertă",
            {
                "fields": (
                    "made_by",
                    "category",
                    "name",
                    "county_coverage",
                    "town",
                    "added_on",
                    "status",
                    
                )
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()

        if (
            request.user.is_superuser
            or request.user.groups.filter(name=DSU_GROUP).exists()
        ):
            return queryset

        if request.user.groups.filter(name=USERS_GROUP).exists():
            return queryset.filter(made_by=request.user)

        return queryset