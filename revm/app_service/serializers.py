from rest_framework import serializers

from .models import ServiceRequest, ServiceResource, Category, Subcategory


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ServiceSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"


class ServiceResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceResource
        fields = "__all__"


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = "__all__"
