from rest_framework import serializers

from available_resources.models import (
    GoodsTransportService,
    OtherResource,
    PeopleTransportService,
    ProductsResource,
    ResourceCategory,
    ResourceSubcategory,
    VolunteeringResource,
)


class ViewCategoriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceCategory
        fields = ("pk", "name")


class ResourceSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceSubcategory
        fields = "__all__"


class ViewCategorySerializer(serializers.ModelSerializer):
    subcategories = ResourceSubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = ResourceCategory
        fields = ("pk", "name", "subcategories")


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
