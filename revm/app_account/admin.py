from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.sites.models import Site

from app_account import models


DjangoUserAdmin.add_fieldsets = (
    (
        None,
        {
            "classes": ("wide",),
            "fields": ("first_name", "last_name", "email", "password1", "password2", "is_staff", "is_superuser"),
        },
    ),
)


class AdminCustomUser(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'phone_number')
    list_display_links = ('id', 'full_name')
    search_fields = ['first_name', 'last_name']

    def full_name(self, obj):
        return obj.__str__()

    full_name.short_description = "Full name"


admin.site.register(models.CustomUser, AdminCustomUser)
admin.site.unregister(Site)
