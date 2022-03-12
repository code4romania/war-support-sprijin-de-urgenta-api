from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from impersonate.admin import UserAdminImpersonateMixin

from app_account.models import CustomUser

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
    (
        _("Location details"),
        {"fields": ("county",)},
    ),
)


@admin.register(CustomUser)
class AdminCustomUser(UserAdminImpersonateMixin, DjangoUserAdmin):
    list_display = ("id", "first_name", "last_name", "email", "phone_number", "type", "user_type", "county")
    list_display_links = ("id", "first_name", "last_name", "email")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_validated", "type")
    ordering = ("first_name",)
    change_form_template = "admin/user_admin.html"
    list_per_page = settings.PAGE_SIZE

    open_new_window = True

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_cncci_user() or request.user.is_cjcci_user():
            return ["is_superuser", "user_permissions", "groups"]
        return self.readonly_fields

    def get_fieldsets(self, request, obj=None):
        if obj:
            return (
                (
                    None,
                    {"fields": ("username", "email")},
                ),
                (
                    _("Personal info"),
                    {"fields": ("first_name", "last_name", "password")},
                ),
                (
                    _("Profile data"),
                    {"fields": ("phone_number", "address")},
                ),
                (
                    _("Permissions"),
                    {"fields": ("is_active", "is_staff", "is_superuser", "user_permissions", "groups")},
                ),
                (
                    _("RVM User"),
                    {"fields": ("type", "business_name", "details", "description")},
                ),
                (
                    _("Location details"),
                    {"fields": ("county",)},
                ),
            )
        else:
            return (
                (
                    None,
                    {"classes": ("wide",), "fields": ("email", "password1", "password2")},
                ),
                (
                    _("Profile data"),
                    {"classes": ("wide",), "fields": ("phone_number", "address")},
                ),
                (
                    _("Profile details"),
                    {"classes": ("wide",), "fields": ("type", "business_name", "identification_no", "groups")},
                ),
            )

    def has_delete_permission(self, request, obj=None):
        if not (request.user.is_superuser):
            return False
        if obj and hasattr(obj, "email"):
            if obj.email == settings.SUPER_ADMIN_EMAIL:
                return False
        return True

    def has_change_permission(self, request, obj=None):
        if not (request.user.is_superuser):
            return False
        if obj and hasattr(obj, "email"):
            if obj.email == settings.SUPER_ADMIN_EMAIL:
                return False
        return True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_cncci_user() or request.user.is_cjcci_user():
            return qs
        return qs.filter(pk=request.user.id)


admin.site.unregister(Site)
