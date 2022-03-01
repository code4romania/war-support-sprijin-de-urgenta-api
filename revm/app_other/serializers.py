from rest_framework import serializers

from .models import OtherRequest, OtherResource, Category, Subcategory


class OtherCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class OtherSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"


class OtherResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherResource
        fields = "__all__"


class OtherRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherRequest
        fields = "__all__"
