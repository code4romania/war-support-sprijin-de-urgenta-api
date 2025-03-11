from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppTransportServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_transport_service"
    verbose_name = _("Transport service")
    verbose_name_plural = _("Transport services")
