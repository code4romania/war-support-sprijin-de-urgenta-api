from django.conf import settings
from rest_framework import serializers
from rest_framework.fields import MultipleChoiceField


class CustomMultipleChoiceField(MultipleChoiceField):
    def to_representation(self, value):
        return list(super().to_representation(value))


class CountyCoverageSerializer(serializers.ModelSerializer):
    county_coverage = CustomMultipleChoiceField(choices=settings.COUNTY_CHOICES)

    class Meta:
        abstract = True
