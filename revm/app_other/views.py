from revm_site.views import CreateResourceViewSet
from .serializers import OtherRequestSerializer, OtherResourceSerializer


class CreateOtherRequestViewSet(CreateResourceViewSet):
    serializer_class = OtherRequestSerializer


class CreateOtherResourceViewSet(CreateResourceViewSet):
    serializer_class = OtherResourceSerializer
