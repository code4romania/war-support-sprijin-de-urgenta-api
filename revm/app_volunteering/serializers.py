from rest_framework import serializers

from app_volunteering.models import VolunteeringRequest, VolunteeringResource


class VolunteeringResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteeringResource
        fields = "__all__"


class VolunteeringRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteeringRequest
        fields = "__all__"
