import logging

from django import http
from django.conf import settings
from django.contrib import messages
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _


class AdminErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("django")

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        self.logger.error(exception)

        if settings.ENVIRONMENT != "production":
            return

        if isinstance(exception, IntegrityError):
            messages.add_message(
                request,
                messages.ERROR,
                _("Delete operation not permitted. Please check that the object is not referenced by other objects."),
            )
            return http.HttpResponseForbidden(_("Integrity error: Delete operation not permitted"))
        return http.HttpResponseForbidden(exception)
