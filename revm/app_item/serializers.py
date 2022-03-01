from rest_framework import serializers

from .models import ItemRequest, ItemResource, Category, Subcategory


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ItemSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"


class ItemResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemResource
        fields = "__all__"


class ItemRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemRequest
        fields = "__all__"
