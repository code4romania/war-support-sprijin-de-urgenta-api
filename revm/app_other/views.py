from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from revm_site.utils.views import CreateResourceViewSet
from .models import Category
from .serializers import (
    OtherRequestSerializer,
    OtherOfferSerializer,
    OtherCategoryListSerializer,
)


class GetOtherCategoryViewSet(ReadOnlyModelViewSet):
    lookup_field = "name"
    permissions_classes = (AllowAny,)

    def get_queryset(self):
        return Category.objects.all().order_by("name")

    def get_serializer_class(self):
        return OtherCategoryListSerializer


class CreateOtherRequestViewSet(CreateResourceViewSet):
    serializer_class = OtherRequestSerializer


class CreateOtherOfferViewSet(CreateResourceViewSet):
    serializer_class = OtherOfferSerializer
