from rest_framework import serializers

from .models import ItemRequest, ItemOffer, Category, Subcategory


class ItemSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"


class ItemCategorySerializer(serializers.ModelSerializer):
    subcategories = ItemSubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class ItemCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ItemOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOffer
        fields = "__all__"


class ItemRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemRequest
        fields = "__all__"
