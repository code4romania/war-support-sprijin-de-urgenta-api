from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

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


admin.site.register(models.CustomUser)
