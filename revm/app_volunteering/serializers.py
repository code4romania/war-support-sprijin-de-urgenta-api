from rest_framework import serializers

from revm_site.serializers import CountyCoverageSerializer
from .models import VolunteeringRequest, VolunteeringOffer, Type


class VolunteeringCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class VolunteeringOfferSerializer(CountyCoverageSerializer):
    class Meta:
        model = VolunteeringOffer
        fields = "__all__"


class VolunteeringRequestSerializer(CountyCoverageSerializer):
    class Meta:
        model = VolunteeringRequest
        fields = "__all__"
