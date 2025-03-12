from django.conf import settings


def environment(_):
    env_label = f"{settings.ENVIRONMENT} | {settings.VERSION_SUFFIX}"
    log_level = settings.DJANGO_LOG_LEVEL

    return env_label, log_level


def dashboard(request, context):
    user = request.user
    context["user_excerpt"] = {
        "name": user.get_full_name(),
        "email": user.email,
    }

    return context
