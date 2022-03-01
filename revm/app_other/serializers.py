from rest_framework import serializers

from .models import OtherRequest, OtherResource


class OtherResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherResource
        fields = "__all__"


class OtherRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherRequest
        fields = "__all__"
