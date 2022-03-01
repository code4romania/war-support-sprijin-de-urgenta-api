from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import (
    TransportServiceRequestSerializer,
    TransportServiceOfferSerializer,
    TransportServiceCategorySerializer,
    TransportServiceSubcategorySerializer,
)
from revm_site.views import CreateResourceViewSet


class GetTransportServiceCategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = TransportServiceCategorySerializer


class GetTransportServiceSubcategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = TransportServiceSubcategorySerializer


class CreateTransportServiceRequestViewSet(CreateResourceViewSet):
    serializer_class = TransportServiceRequestSerializer


class CreateTransportServiceOfferViewSet(CreateResourceViewSet):
    serializer_class = TransportServiceOfferSerializer
