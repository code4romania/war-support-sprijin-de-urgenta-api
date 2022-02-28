from django.core.cache import caches
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from donors.serializers import CreateDonorSerializer


class CreateDonorQueryBurstAnonRateThrottle(AnonRateThrottle):
    cache = caches["default"]
    rate = "20/min"


class CreateDonorViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    throttle_classes = (CreateDonorQueryBurstAnonRateThrottle,)
    serializer_class = CreateDonorSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateDonorSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
