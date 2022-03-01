from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from revm_site.views import CreateResourceViewSet
from .models import Subcategory, Category
from .serializers import (
    OtherRequestSerializer,
    OtherOfferSerializer,
    OtherCategorySerializer,
    OtherSubcategorySerializer,
)


class GetOtherCategoryViewSet(ReadOnlyModelViewSet):
    lookup_field = "name"
    permissions_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = OtherCategorySerializer


class GetOtherSubcategoryViewSet(ReadOnlyModelViewSet):
    lookup_field = "name"
    permissions_classes = (AllowAny,)
    queryset = Subcategory.objects.all()
    serializer_class = OtherSubcategorySerializer


class CreateOtherRequestViewSet(CreateResourceViewSet):
    serializer_class = OtherRequestSerializer


class CreateOtherOfferViewSet(CreateResourceViewSet):
    serializer_class = OtherOfferSerializer
