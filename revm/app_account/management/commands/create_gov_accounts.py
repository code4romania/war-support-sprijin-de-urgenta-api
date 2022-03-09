import csv
import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from app_account.models import CustomUser, CJCCI_GROUP, CNCCI_GROUP

logger = logging.getLogger("django")

class Command(BaseCommand):

    @staticmethod
    def create_user(row):
        is_cncci = row[0] == 'CNCCI'
        # extract from row
        first_name = row[0]
        last_name = row[0] if is_cncci else 'CJCCI'
        email = row[1].strip()
        password = row[2].strip()

        group_name = CNCCI_GROUP if is_cncci else CJCCI_GROUP

        # no CustomUser.get_or_create()
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = CustomUser(email=email)

        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        user.is_superuser = False
        # user.is_staff = is_cncci
        user.is_staff = False
        user.is_validated = True

        user.set_password(password)

        user.save()

        # group roles
        user.groups.add(Group.objects.get(name=CNCCI_GROUP))

    def handle(self, *args, **kwargs):
        try:
            file = open(settings.BASE_DIR + '/data.csv')
        except Exception as e:
            logger.info('Could not find file data.csv')
            return

        csvreader = csv.reader(file)

        for row in csvreader:
            print(row)
            self.create_user(row[0].split(';'))
