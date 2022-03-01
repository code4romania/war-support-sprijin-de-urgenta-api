from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from revm_site.views import CreateResourceViewSet
from .models import Type
from .serializers import VolunteeringRequestSerializer, VolunteeringOfferSerializer, VolunteeringCategorySerializer


class GetVolunteeringCategoryViewSet(ReadOnlyModelViewSet):
    lookup_field = "name"
    permissions_classes = (AllowAny,)
    queryset = Type.objects.all()
    serializer_class = VolunteeringCategorySerializer


class CreateVolunteeringRequestViewSet(CreateResourceViewSet):
    serializer_class = VolunteeringRequestSerializer


class CreateVolunteeringOfferViewSet(CreateResourceViewSet):
    serializer_class = VolunteeringOfferSerializer
