from rest_framework import serializers

from .models import TransportServiceRequest, TransportServiceOffer, Category, Subcategory


class TransportServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TransportServiceSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"


class TransportServiceOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportServiceOffer
        fields = "__all__"


class TransportServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportServiceRequest
        fields = "__all__"
