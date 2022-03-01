from .serializers import ServiceRequestSerializer, ServiceResourceSerializer
from revm_site.views import CreateResourceViewSet


class CreateServiceRequestViewSet(CreateResourceViewSet):
    serializer_class = ServiceRequestSerializer


class CreateServiceResourceViewSet(CreateResourceViewSet):
    serializer_class = ServiceResourceSerializer
