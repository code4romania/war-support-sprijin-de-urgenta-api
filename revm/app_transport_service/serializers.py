from rest_framework import serializers

from .models import TransportServiceRequest, TransportServiceResource


class TransportServiceResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportServiceResource
        fields = "__all__"


class TransportServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportServiceRequest
        fields = "__all__"
