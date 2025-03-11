from rest_framework import serializers

from revm_site.utils.serializers import CountyCoverageSerializer
from .models import TransportServiceRequest, TransportServiceOffer, Category


class TransportServiceCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TransportServiceOfferSerializer(CountyCoverageSerializer):
    class Meta:
        model = TransportServiceOffer
        fields = "__all__"


class TransportServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportServiceRequest
        fields = "__all__"
