from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from available_resources.serializers import (
    CreateGoodsTransportServiceSerializer,
    CreatePeopleTransportServiceSerializer,
    CreateFoodProductsResourceSerializer,
)


class CreateGoodsTransportServiceViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    throttle_classes = (AnonRateThrottle,)
    serializer_class = CreateGoodsTransportServiceSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateGoodsTransportServiceSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CreatePeopleTransportServiceViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    throttle_classes = (AnonRateThrottle,)
    serializer_class = CreatePeopleTransportServiceSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreatePeopleTransportServiceSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CreateFoodProductsResourceViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    throttle_classes = (AnonRateThrottle,)
    serializer_class = CreateFoodProductsResourceSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateFoodProductsResourceSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
