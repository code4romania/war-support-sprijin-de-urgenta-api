from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from available_resources.serializers import (
    CreateGoodsTransportServiceSerializer,
    CreatePeopleTransportServiceSerializer,
    CreateProductsResourceSerializer,
)
from available_resources.serializers import CreateOtherResourceSerializer
from available_resources.serializers import CreateVolunteeringResourceSerializer


class CreateResourceViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
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
