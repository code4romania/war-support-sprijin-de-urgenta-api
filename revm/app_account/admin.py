from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404, render
from django.conf.urls import url
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

# def user_offers_view(request, model_admin, object):
#     print('****')
#     print(request.POST)
#     print('****')
#     model = model_admin.model
#     opts = model._meta
#     return render(
#         request,
#         'app_account/user_offers.html', {
#             'opts': opts,
#             'has_change_permission': model_admin.has_change_permission(request, object),
#             'original': object,
#         }
#     )

@admin.register(models.CustomUser)
class AdminCustomUser(DjangoUserAdmin):
    list_display = ("id", "first_name", "last_name", "email", "phone_number")
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
                (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "user_permissions")}),
                (
                    _("RVM User"),
                    {"fields": ("type", "business_name", "phone_number", "address", "details", "description")},
                ),
            )
        else:
            return self.add_fieldsets

    def has_delete_permission(self, request, obj=None):
        if obj and hasattr(obj, "email"):
            if obj.email == settings.SUPER_ADMIN_EMAIL:
                return False
        return True


    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     user = models.CustomUser.objects.get(pk=object_id)
        
    #     extra_context['user'] = user
    #     return super().change_view(
    #         request, object_id, form_url, extra_context=extra_context,
    #     )



    # def get_urls(self):
    #     info = self.model._meta.app_label, self.model._meta.model_name
    #     urls = super().get_urls()
    #     my_urls = [

    #         url(r'^(?P<object_id>.*)/offers/$',
    #         self.admin_site.admin_view(self.user_offers), {},
    #         name="%s_%s_schema" % info),
    #     ]
    #     return my_urls + urls

    # def user_offers(self, request, object_id):
    #     user = get_object_or_404(models.CustomUser, id=int(object_id))

    #     print('****')
    #     print(request.POST)
    #     print('****')
    #     return user_offers_view(request, self, user)
    #     return render(request, "app_account/user_offers.html", context)



admin.site.unregister(Site)
