import requests
from django.conf import settings
from django.utils import timezone
from django.utils.log import AdminEmailHandler


class SlackHandler(AdminEmailHandler):
    def send_mail(self, subject, message, *args, **kwargs):
        if not settings.ENABLE_SLACK_LOGGING:
            return

        slack_payload = {
            "color": f"#{settings.SLACK_LOGGING_COLOR}",
            "fallback": "SdU Site Error",
            "pretext": ":this-is-fine: An error occurred on the server",
            "fields": [
                {
                    "title": "Error message:",
                    "value": "```{}```".format(subject),
                    "short": False,
                },
                {
                    "title": "ENVIRONMENT",
                    "value": settings.ENVIRONMENT,
                    "short": True,
                },
                {
                    "title": "TIME OCCURRED",
                    "value": f"{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    "short": True,
                },
            ],
        }

        requests.post(settings.SLACK_WEBHOOK_URL, json=slack_payload)
