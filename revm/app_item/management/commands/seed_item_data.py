import os
import json

from django.core.management.base import BaseCommand

from app_item.models import Category, TextileCategory


class Command(BaseCommand):
    @staticmethod
    def populate_item_categories_and_subcategories():
        base_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(base_path, "item_data.json")
        with open(file_path) as f:
            categories = json.load(f)

            for category in categories:
                category_obj, _ = Category.objects.get_or_create(name=category["name"])

        file_path = os.path.join(base_path, "item_textile_data.json")
        with open(file_path) as f:
            categories = json.load(f)

            for category in categories:
                category_obj, _ = TextileCategory.objects.get_or_create(name=category["name"])

    def handle(self, *args, **kwargs):
        self.populate_item_categories_and_subcategories()
        print("Item Categories & Subcategories created")
