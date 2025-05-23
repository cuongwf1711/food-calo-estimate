# Copyright (C)
# date: 12-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Input Image View Set."""

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from FoodCaloEstimate.estimator.models.my_input_image import MyInputImage
from FoodCaloEstimate.estimator.serializers.input_image_serializer import (
    InputImageSerializer,
)
from FoodCaloEstimate.estimator.utils.my_input_image_pagination import (
    MyInputImagePagination,
)
from FoodCaloEstimate.estimator.view_filters.input_image_filter import (
    InputImageFilter,
)


class InputImageViewSet(viewsets.ModelViewSet):
    """Input Image View Set."""

    queryset = MyInputImage.objects.filter(is_deleted=False)
    serializer_class = InputImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]
    pagination_class = MyInputImagePagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = InputImageFilter
    ordering_fields = ["calo", "created_at"]

    def destroy(self, request, *args, **kwargs):
        """Soft delete the input image."""
        instance = self.get_object()
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
