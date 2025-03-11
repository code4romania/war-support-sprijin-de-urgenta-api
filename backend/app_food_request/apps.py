from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppFoodRequestConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_food_request"
    verbose_name = _("NGO food request")
    verbose_name_plural = _("NGO food requests")
