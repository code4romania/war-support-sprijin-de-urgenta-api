from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from revm_site.views import CreateResourceViewSet
from .models import Category, Subcategory
from .serializers import (
    ItemRequestSerializer,
    ItemOfferSerializer,
    ItemCategorySerializer,
    ItemSubcategorySerializer,
)


class GetItemCategoryViewSet(ReadOnlyModelViewSet):
    lookup_field = "name"
    permissions_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = ItemCategorySerializer


class GetItemSubcategoryViewSet(ReadOnlyModelViewSet):
    lookup_field = "name"
    permissions_classes = (AllowAny,)
    queryset = Subcategory.objects.all()
    serializer_class = ItemSubcategorySerializer


class CreateItemRequestViewSet(CreateResourceViewSet):
    serializer_class = ItemRequestSerializer


class CreateItemOfferViewSet(CreateResourceViewSet):
    serializer_class = ItemOfferSerializer
