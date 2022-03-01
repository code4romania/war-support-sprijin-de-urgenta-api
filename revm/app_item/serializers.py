from rest_framework import serializers

from .models import ItemRequest, ItemOffer, Category, Subcategory


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ItemSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"


class ItemOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOffer
        fields = "__all__"


class ItemRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemRequest
        fields = "__all__"
