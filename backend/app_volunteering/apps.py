from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppVolunteeringConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_volunteering"
    verbose_name = _("Volunteering")
    verbose_name_plural = _("Volunteering")
