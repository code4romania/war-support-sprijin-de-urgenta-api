from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from revm_site.utils.views import CreateResourceViewSet
from .models import Category
from .serializers import VolunteeringRequestSerializer, VolunteeringOfferSerializer, VolunteeringCategorySerializer


class GetVolunteeringCategoryViewSet(ReadOnlyModelViewSet):
    lookup_field = "name"
    permissions_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = VolunteeringCategorySerializer


class CreateVolunteeringRequestViewSet(CreateResourceViewSet):
    serializer_class = VolunteeringRequestSerializer


class CreateVolunteeringOfferViewSet(CreateResourceViewSet):
    serializer_class = VolunteeringOfferSerializer
