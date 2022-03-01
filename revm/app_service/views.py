from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import (
    ServiceRequestSerializer,
    ServiceOfferSerializer,
    ServiceCategorySerializer,
    ServiceSubcategorySerializer,
)
from revm_site.views import CreateResourceViewSet


class GetServiceCategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = ServiceCategorySerializer


class GetServiceSubcategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = ServiceSubcategorySerializer


class CreateServiceRequestViewSet(CreateResourceViewSet):
    serializer_class = ServiceRequestSerializer


class CreateServiceOfferViewSet(CreateResourceViewSet):
    serializer_class = ServiceOfferSerializer
