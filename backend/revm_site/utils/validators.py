from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_date_disallow_past(date):
    err_message = _("Date cannot be in the past")
    if isinstance(date, timezone.datetime):
        if date < timezone.localtime():
            raise ValidationError(err_message)
    if date < timezone.localtime().date():
        raise ValidationError(err_message)
