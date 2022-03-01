from django.contrib import admin
from app_other import models

admin.site.register(models.Category)
admin.site.register(models.Subcategory)
admin.site.register(models.OtherResource)
admin.site.register(models.OtherRequest)
