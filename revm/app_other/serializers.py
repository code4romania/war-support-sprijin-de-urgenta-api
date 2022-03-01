from rest_framework import serializers

from .models import OtherRequest, OtherOffer, Category, Subcategory


class OtherSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"


class OtherCategorySerializer(serializers.ModelSerializer):
    subcategories = OtherSubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class OtherCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class OtherOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherOffer
        fields = "__all__"


class OtherRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherRequest
        fields = "__all__"
