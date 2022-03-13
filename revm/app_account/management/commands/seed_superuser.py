from django.conf import settings
from django.core.management.base import BaseCommand

from app_account.models import CustomUser


class Command(BaseCommand):
    @staticmethod
    def create_superuser():
        admin_user = CustomUser.objects.filter(is_superuser=True)

        if not admin_user:
            superuser = CustomUser()
            superuser.is_active = True
            superuser.is_superuser = True
            superuser.is_staff = True
            superuser.email = settings.SUPER_ADMIN_EMAIL
            superuser.first_name = settings.SUPER_ADMIN_FIRST_NAME
            superuser.last_name = settings.SUPER_ADMIN_LAST_NAME
            superuser.set_password(settings.SUPER_ADMIN_PASS)
            superuser.type = CustomUser.NON_PROFIT
            superuser.save()
        else:
            print("Super admin user already exists")

    def handle(self, *args, **kwargs):
        self.create_superuser()
        print("Super admin has been created")
