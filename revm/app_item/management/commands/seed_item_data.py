import os
import json

from django.core.management.base import BaseCommand

from app_item.models import Category, TextileCategory


class Command(BaseCommand):
    @staticmethod
    def populate_item_categories_and_subcategories():
        base_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(base_path, "item_data.json")
        Command._populate_categories(file_path, Category)

        file_path = os.path.join(base_path, "item_textile_data.json")
        Command._populate_categories(file_path, TextileCategory)

    @staticmethod
    def _populate_categories(file_path, category_class):
        with open(file_path) as f:
            categories = json.load(f)

            for category in categories:
                category_obj, _ = category_class.objects.get_or_create(
                    name=category["name"],
                    name_ro=category["name_ro"],
                    name_en=category["name_en"],
                    name_ru=category["name_ru"],
                    name_uk=category["name_uk"],
                )

    def handle(self, *args, **kwargs):
        self.populate_item_categories_and_subcategories()
        print("Item Categories & Subcategories created")
