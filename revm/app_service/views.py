from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Category, Subcategory
from .serializers import (
    ServiceRequestSerializer,
    ServiceResourceSerializer,
    ServiceCategorySerializer,
    ServiceSubcategorySerializer,
)
from revm_site.views import CreateResourceViewSet


class GetServiceCategoryViewSet(ReadOnlyModelViewSet):
    lookup_field = "name"
    permissions_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = ServiceCategorySerializer


class GetServiceSubcategoryViewSet(ReadOnlyModelViewSet):
    lookup_field = "name"
    permissions_classes = (AllowAny,)
    queryset = Subcategory.objects.all()
    serializer_class = ServiceSubcategorySerializer


class CreateServiceRequestViewSet(CreateResourceViewSet):
    serializer_class = ServiceRequestSerializer


class CreateServiceResourceViewSet(CreateResourceViewSet):
    serializer_class = ServiceResourceSerializer
