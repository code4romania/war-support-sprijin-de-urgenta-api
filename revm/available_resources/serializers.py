from rest_framework import serializers

from available_resources.models import GoodsTransportService, PeopleTransportService, FoodProductsResource


class CreateGoodsTransportServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsTransportService
        fields = "__all__"


class CreatePeopleTransportServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeopleTransportService
        fields = "__all__"


class CreateFoodProductsResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodProductsResource
        fields = "__all__"
