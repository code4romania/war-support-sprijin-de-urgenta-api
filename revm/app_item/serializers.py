from rest_framework import serializers

from .models import ItemRequest, ItemOffer, Category


class ItemCategorySerializer(serializers.ModelSerializer):

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
