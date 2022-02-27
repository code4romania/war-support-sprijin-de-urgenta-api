from rest_framework import serializers
from donors.models import Donor


class CreateDonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = "__all__"
