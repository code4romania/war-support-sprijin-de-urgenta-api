from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppItemConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_item"
    verbose_name = _("Item")
    verbose_name_plural = _("Items")
