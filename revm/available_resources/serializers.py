from rest_framework import serializers

from available_resources.models import GoodsTransportService, PeopleTransportService, ProductsResource
from available_resources.models import OtherResource
from available_resources.models import VolunteeringResource


class CreateGoodsTransportServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsTransportService
        fields = "__all__"


class CreatePeopleTransportServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeopleTransportService
        fields = "__all__"


class CreateProductsResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsResource
        fields = "__all__"


class CreateVolunteeringResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteeringResource
        fields = "__all__"


class CreateOtherResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherResource
        fields = "__all__"
