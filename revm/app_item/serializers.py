from rest_framework import serializers

from .models import ItemRequest, ItemResource


class ItemResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemResource
        fields = "__all__"


class ItemRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemRequest
        fields = "__all__"
