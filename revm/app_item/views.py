from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from revm_site.views import CreateResourceViewSet
from .models import Category
from .serializers import (
    ItemRequestSerializer,
    ItemOfferSerializer,
    ItemCategorySerializer,
    ItemCategoryListSerializer,
)


class GetItemCategoryViewSet(ReadOnlyModelViewSet):
    lookup_field = "name"
    permissions_classes = (AllowAny,)

    def get_queryset(self):
        return Category.objects.all().order_by("name")

    def get_serializer_class(self):
        if self.action == "list":
            return ItemCategoryListSerializer
        return ItemCategorySerializer


class CreateItemRequestViewSet(CreateResourceViewSet):
    serializer_class = ItemRequestSerializer


class CreateItemOfferViewSet(CreateResourceViewSet):
    serializer_class = ItemOfferSerializer
