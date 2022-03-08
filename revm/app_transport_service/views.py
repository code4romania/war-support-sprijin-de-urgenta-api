from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from revm_site.utils.views import CreateResourceViewSet
from .models import Category
from .serializers import (
    TransportServiceRequestSerializer,
    TransportServiceOfferSerializer,
    TransportServiceCategoryListSerializer,
)


class GetTransportServiceCategoryViewSet(ReadOnlyModelViewSet):
    lookup_field = "name"
    permissions_classes = (AllowAny,)

    def get_queryset(self):
        return Category.objects.all().order_by("name")

    def get_serializer_class(self):
        return TransportServiceCategoryListSerializer


class CreateTransportServiceRequestViewSet(CreateResourceViewSet):
    serializer_class = TransportServiceRequestSerializer


class CreateTransportServiceOfferViewSet(CreateResourceViewSet):
    serializer_class = TransportServiceOfferSerializer
