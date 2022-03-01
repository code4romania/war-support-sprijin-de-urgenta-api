from rest_framework import serializers

from .models import ServiceRequest, ServiceOffer, Category, Subcategory


class ServiceSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"


class ServiceCategorySerializer(serializers.ModelSerializer):
    subcategories = ServiceSubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class ServiceCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ServiceOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOffer
        fields = "__all__"


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = "__all__"
