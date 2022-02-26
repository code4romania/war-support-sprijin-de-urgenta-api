from django.conf import settings
from django.contrib import admin, messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.translation import ngettext


def send_email(template: str, context: dict, subject: str, to: str):
    html = get_template(template)
    html_content = html.render(context)

    from_email = settings.NO_REPLY_EMAIL if hasattr(settings, "NO_REPLY_EMAIL") else settings.DEFAULT_FROM_EMAIL
    headers = {"X-SES-CONFIGURATION-SET": "centre-testare-hiv"}

    msg = EmailMultiAlternatives(subject, html_content, from_email, [to], headers=headers)
    msg.attach_alternative(html_content, "text/html")

    return msg.send(fail_silently=True)


class AdminWithStatusChanges(admin.ModelAdmin):
    def _perform_status_change(self, status, request, queryset, item_status_choices, item_singular, item_plural):
        updated = queryset.update(status=status)

        status_str = self.choice_to_string(status, item_status_choices)
        message = ngettext(
            "{updated} {item_sg} was successfully marked as {status}.",
            "{updated} {item_pl} were successfully marked as {status}.",
            updated,
        ).format(updated=updated, status=status_str, item_sg=item_singular, item_pl=item_plural)

        self.message_user(request, message, messages.SUCCESS)

    @staticmethod
    def choice_to_string(status, choices):
        status = int(status)
        for status_choice in choices:
            if status_choice[0] == status:
                status_str = status_choice[1]
                break
        else:
            status_str = ""
        return status_str
