from rest_framework import serializers

from revm_site.serializers import CountyCoverageSerializer
from .models import OtherRequest, OtherOffer, Category


class OtherCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class OtherOfferSerializer(CountyCoverageSerializer):
    class Meta:
        model = OtherOffer
        fields = "__all__"


class OtherRequestSerializer(CountyCoverageSerializer):
    class Meta:
        model = OtherRequest
        fields = "__all__"
