from rest_framework.viewsets import ReadOnlyModelViewSet

from revm_site.views import CreateResourceViewSet
from .serializers import (
    ItemRequestSerializer,
    ItemOfferSerializer,
    ItemCategorySerializer,
    ItemSubcategorySerializer,
)


class GetItemCategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = ItemCategorySerializer


class GetItemSubcategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = ItemSubcategorySerializer


class CreateItemRequestViewSet(CreateResourceViewSet):
    serializer_class = ItemRequestSerializer


class CreateItemOfferViewSet(CreateResourceViewSet):
    serializer_class = ItemOfferSerializer
