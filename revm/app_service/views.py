from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Category, Subcategory
from .serializers import (
    ServiceRequestSerializer,
    ServiceOfferSerializer,
    ServiceCategorySerializer,
    ServiceSubcategorySerializer,
    ServiceCategoryListSerializer,
)
from revm_site.views import CreateResourceViewSet


class GetServiceCategoryViewSet(ReadOnlyModelViewSet):
    lookup_field = "name"
    permissions_classes = (AllowAny,)

    def get_queryset(self):
        return Category.objects.all().order_by("name")

    def get_serializer_class(self):
        if self.action == "list":
            return ServiceCategoryListSerializer
        return ServiceCategorySerializer


class GetServiceSubcategoryViewSet(ReadOnlyModelViewSet):
    lookup_field = "name"
    permissions_classes = (AllowAny,)
    queryset = Subcategory.objects.all()
    serializer_class = ServiceSubcategorySerializer


class CreateServiceRequestViewSet(CreateResourceViewSet):
    serializer_class = ServiceRequestSerializer


class CreateServiceOfferViewSet(CreateResourceViewSet):
    serializer_class = ServiceOfferSerializer
