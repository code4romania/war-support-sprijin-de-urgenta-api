from rest_framework import serializers

from .models import VolunteeringRequest, VolunteeringOffer, Type


class VolunteeringCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class VolunteeringOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteeringOffer
        fields = "__all__"


class VolunteeringRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteeringRequest
        fields = "__all__"
