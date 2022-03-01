from rest_framework import serializers

from .models import TransportServiceRequest, TransportServiceOffer, Category, Subcategory


class TransportServiceSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"


class TransportServiceCategorySerializer(serializers.ModelSerializer):
    subcategories = TransportServiceSubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class TransportServiceCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TransportServiceOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportServiceOffer
        fields = "__all__"


class TransportServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportServiceRequest
        fields = "__all__"
