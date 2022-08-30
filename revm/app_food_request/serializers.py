from rest_framework import serializers

from revm_site.utils.serializers import CountyCoverageSerializer
from app_food_request.models import FoodRequest


class FoodRequestSerializer(CountyCoverageSerializer):
    class Meta:
        model = FoodRequest
        fields = "__all__"
