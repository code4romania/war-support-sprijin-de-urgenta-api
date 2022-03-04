from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

from app_account import models

DjangoUserAdmin.add_fieldsets = (
    (
        _("Personal info"),
        {"classes": ("wide",), "fields": ("first_name", "last_name", "email")},
    ),
    (
        _("Password"),
        {"classes": ("wide",), "fields": ("password1", "password2")},
    ),
    (
        _("Permissions"),
        {"classes": ("wide",), "fields": ("is_staff", "is_superuser", "groups")},
    ),
)


@admin.register(models.CustomUser)
class AdminCustomUser(DjangoUserAdmin):
    list_display = ("id", "first_name", "last_name", "email", "phone_number", "type")
    list_display_links = ["id", "first_name", "last_name", "email"]
    search_fields = ("email", "first_name", "last_name")
    list_filter = ["is_validated"]

    ordering = ("first_name",)
    change_form_template = "admin/user_admin.html"

    def get_fieldsets(self, request, obj=None):
        if obj:
            return (
                (
                    None,
                    {
                        "fields": (
                            "username",
                            "email",
                        )
                    },
                ),
                (_("Personal info"), {"fields": ("first_name", "last_name", "password")}),
                (_("Profile data"), {"fields": ("phone_number", "address")}),
                # Restricting Set Superuser to superuser
                (
                    _("Permissions"),
                    {
                        "fields": ("is_active", "is_staff", "is_superuser", "user_permissions", "groups")
                        if request.user.is_superuser
                        else ("is_active", "is_staff")
                    },
                ),
                (
                    _("RVM User"),
                    {"fields": ("type", "business_name", "phone_number", "address", "details", "description")},
                ),
            )
        else:
            return self.add_fieldsets

    def has_delete_permission(self, request, obj=None):
        if not (request.user.is_superuser or request.user.groups.filter(name=models.DSU_MANAGER_GROUP).exists()):
            return False
        if obj and hasattr(obj, "email"):
            if obj.email == settings.SUPER_ADMIN_EMAIL:
                return False
        return True

    def has_change_permission(self, request, obj=None):
        if not (request.user.is_superuser or request.user.groups.filter(name=models.DSU_MANAGER_GROUP).exists()):
            return False
        if obj and hasattr(obj, "email"):
            if obj.email == settings.SUPER_ADMIN_EMAIL:
                return False
        return True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name=models.DSU_MANAGER_GROUP).exists():
            return qs
        return qs.filter(pk=request.user.id)


admin.site.unregister(Site)
