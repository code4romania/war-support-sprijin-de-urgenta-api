from rest_framework import serializers

from .models import OtherRequest, OtherOffer, Category


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
