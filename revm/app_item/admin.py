from django.contrib import admin
from app_item import models


admin.site.register(models.Category)
admin.site.register(models.Subcategory)
admin.site.register(models.ItemResource)
admin.site.register(models.ItemRequest)
