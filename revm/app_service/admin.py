from django.contrib import admin
from app_service import models

admin.site.register(models.Category)
admin.site.register(models.Subcategory)
admin.site.register(models.ServiceResource)
admin.site.register(models.ServiceRequest)
