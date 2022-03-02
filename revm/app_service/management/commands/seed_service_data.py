import os
import json

from django.core.management.base import BaseCommand

from app_service.models import Category, Subcategory


class Command(BaseCommand):
    @staticmethod
    def populate_service_categories_and_subcategories():
        base_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(base_path, 'service_data.json')
        with open(file_path) as f:
            categories = json.load(f)

            for category in categories:
                category_obj = Category.objects.create(name=category['name'],
                                                       description=category.get('description', ''))
                for subcategory in category['subcategories']:
                    Subcategory(category=category_obj,
                                name=subcategory['name'],
                                description=subcategory.get('description', '')).save()

    def handle(self, *args, **kwargs):
        self.populate_service_categories_and_subcategories()
        print('Service Categories & Subcategories created')
