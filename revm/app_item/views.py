from revm_site.views import CreateResourceViewSet
from .serializers import ItemRequestSerializer, ItemResourceSerializer


class CreateItemRequestViewSet(CreateResourceViewSet):
    serializer_class = ItemRequestSerializer


class CreateItemResourceViewSet(CreateResourceViewSet):
    serializer_class = ItemResourceSerializer
