from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from available_resources.models import ResourceCategory
from available_resources.serializers import (
    CreateGoodsTransportServiceSerializer,
    CreateOtherResourceSerializer,
    CreatePeopleTransportServiceSerializer,
    CreateProductsResourceSerializer,
    CreateVolunteeringResourceSerializer,
    ViewCategoriesListSerializer,
    ViewCategorySerializer,
)


class CategoriesViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "pk"
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ResourceCategory.objects.all().order_by("name")

    def get_serializer_class(self):
        if self.action == "list":
            return ViewCategoriesListSerializer
        return ViewCategorySerializer


class CategoriesByNameViewSet(CategoriesViewSet):
    lookup_field = "name"


class CreateResourceViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    throttle_classes = (AnonRateThrottle,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CreateGoodsTransportServiceViewSet(CreateResourceViewSet):
    serializer_class = CreateGoodsTransportServiceSerializer


class CreatePeopleTransportServiceViewSet(CreateResourceViewSet):
    serializer_class = CreatePeopleTransportServiceSerializer


class CreateProductsResourceViewSet(CreateResourceViewSet):
    serializer_class = CreateProductsResourceSerializer


class CreateVolunteeringResourceViewSet(CreateResourceViewSet):
    serializer_class = CreateVolunteeringResourceSerializer


class CreateOtherResourceViewSet(CreateResourceViewSet):
    serializer_class = CreateOtherResourceSerializer
