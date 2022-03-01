from app_volunteering.serializers import VolunteeringRequestSerializer, VolunteeringResourceSerializer
from revm_site.views import CreateResourceViewSet


class CreateVolunteeringRequestViewSet(CreateResourceViewSet):
    serializer_class = VolunteeringRequestSerializer


class CreateVolunteeringResourceViewSet(CreateResourceViewSet):
    serializer_class = VolunteeringResourceSerializer
