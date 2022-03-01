from rest_framework import serializers

from .models import VolunteeringRequest, VolunteeringResource, Type


class VolunteeringCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class VolunteeringResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteeringResource
        fields = "__all__"


class VolunteeringRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteeringRequest
        fields = "__all__"
