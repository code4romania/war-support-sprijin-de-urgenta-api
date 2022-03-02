import os
import json

from django.core.management.base import BaseCommand

from app_volunteering.models import Type


class Command(BaseCommand):
    @staticmethod
    def populate_volunteering_types():
        base_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(base_path, 'volunteering_types.json')
        with open(file_path) as f:
            categories = json.load(f)

            for category in categories:
                Type(name=category['name']).save()

    def handle(self, *args, **kwargs):
        self.populate_volunteering_types()
        print('Volunteering Types created')
