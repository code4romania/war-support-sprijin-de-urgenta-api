from rest_framework import serializers

from available_resources.models import Resource


class CreateResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"
