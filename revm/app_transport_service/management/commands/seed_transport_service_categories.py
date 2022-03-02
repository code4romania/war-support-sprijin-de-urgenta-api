import os
import json

from django.core.management.base import BaseCommand

from app_transport_service.models import Category


class Command(BaseCommand):
    @staticmethod
    def populate_transport_service_categories():
        base_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(base_path, "transport_service_categories.json")
        with open(file_path) as f:
            categories = json.load(f)

            for category in categories:
                Category.objects.get_or_create(name=category["name"])

    def handle(self, *args, **kwargs):
        self.populate_transport_service_categories()
        print("Transport Service Categories created")
