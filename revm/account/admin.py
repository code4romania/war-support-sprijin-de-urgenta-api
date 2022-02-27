from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from account import models


DjangoUserAdmin.add_fieldsets = (
    (
        None,
        {
            "classes": ("wide",),
            "fields": ("first_name", "last_name", "email", "password1", "password2", "is_staff", "is_superuser"),
        },
    ),
)


@admin.register(models.CustomUser)
class AdminCustomUser(DjangoUserAdmin):
    list_display = ("id", "first_name", "last_name", "email")
    list_display_links = ["id", "first_name", "last_name", "email"]
    search_fields = ("email", "first_name", "last_name")
    ordering = ("first_name",)

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
                (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "user_permissions")}),
            )
        else:
            return self.add_fieldsets

    def has_delete_permission(self, request, obj=None):
        if obj and hasattr(obj, "email"):
            if obj.email == settings.SUPER_ADMIN_EMAIL:
                return False
        return True


admin.site.unregister(Group)
