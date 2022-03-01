from django.contrib import admin
from app_volunteering import models

admin.site.register(models.Type)
admin.site.register(models.VolunteeringResource)
admin.site.register(models.VolunteeringRequest)
