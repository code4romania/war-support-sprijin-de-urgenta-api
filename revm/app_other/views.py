from rest_framework.viewsets import ReadOnlyModelViewSet

from revm_site.views import CreateResourceViewSet
from .serializers import (
    OtherRequestSerializer,
    OtherResourceSerializer,
    OtherCategorySerializer,
    OtherSubcategorySerializer,
)


class GetOtherCategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = OtherCategorySerializer


class GetOtherSubcategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = OtherSubcategorySerializer


class CreateOtherRequestViewSet(CreateResourceViewSet):
    serializer_class = OtherRequestSerializer


class CreateOtherResourceViewSet(CreateResourceViewSet):
    serializer_class = OtherResourceSerializer
