from rest_framework.viewsets import ReadOnlyModelViewSet

from revm_site.views import CreateResourceViewSet
from .serializers import VolunteeringRequestSerializer, VolunteeringResourceSerializer, VolunteeringCategorySerializer


class GetVolunteeringCategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = VolunteeringCategorySerializer


class CreateVolunteeringRequestViewSet(CreateResourceViewSet):
    serializer_class = VolunteeringRequestSerializer


class CreateVolunteeringResourceViewSet(CreateResourceViewSet):
    serializer_class = VolunteeringResourceSerializer
