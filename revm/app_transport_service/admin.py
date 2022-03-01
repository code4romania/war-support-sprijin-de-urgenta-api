from django.contrib import admin
from app_transport_service import models

admin.site.register(models.Category)
admin.site.register(models.Subcategory)
admin.site.register(models.TransportServiceRequest)
admin.site.register(models.TransportServiceResource)
