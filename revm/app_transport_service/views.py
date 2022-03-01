from .serializers import TransportServiceRequestSerializer, TransportServiceResourceSerializer
from revm_site.views import CreateResourceViewSet


class CreateTransportServiceRequestViewSet(CreateResourceViewSet):
    serializer_class = TransportServiceRequestSerializer


class CreateTransportServiceResourceViewSet(CreateResourceViewSet):
    serializer_class = TransportServiceResourceSerializer
