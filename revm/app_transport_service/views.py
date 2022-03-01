from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Category, Subcategory
from .serializers import (
    TransportServiceRequestSerializer,
    TransportServiceOfferSerializer,
    TransportServiceCategorySerializer,
    TransportServiceSubcategorySerializer,
)
from revm_site.views import CreateResourceViewSet


class GetTransportServiceCategoryViewSet(ReadOnlyModelViewSet):
    lookup_field = "name"
    permissions_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = TransportServiceCategorySerializer


class GetTransportServiceSubcategoryViewSet(ReadOnlyModelViewSet):
    lookup_field = "name"
    permissions_classes = (AllowAny,)
    queryset = Subcategory.objects.all()
    serializer_class = TransportServiceSubcategorySerializer


class CreateTransportServiceRequestViewSet(CreateResourceViewSet):
    serializer_class = TransportServiceRequestSerializer


class CreateTransportServiceOfferViewSet(CreateResourceViewSet):
    serializer_class = TransportServiceOfferSerializer
