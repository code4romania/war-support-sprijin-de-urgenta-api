import json
import os

from django.core.management.base import BaseCommand

from app_volunteering.models import Category


class Command(BaseCommand):
    @staticmethod
    def populate_volunteering_types():
        base_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(base_path, "volunteering_types.json")
        with open(file_path) as f:
            categories = json.load(f)

            for category in categories:
                Category.objects.get_or_create(
                    name=category["name"],
                    name_ro=category["name_ro"],
                    name_en=category["name_en"],
                    name_ru=category["name_ru"],
                    name_uk=category["name_uk"],
                )

    def handle(self, *args, **kwargs):
        self.populate_volunteering_types()
        print("Volunteering Types created")
