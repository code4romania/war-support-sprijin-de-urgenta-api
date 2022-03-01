from rest_framework import serializers

from .models import ServiceRequest, ServiceResource


class ServiceResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceResource
        fields = "__all__"


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = "__all__"
