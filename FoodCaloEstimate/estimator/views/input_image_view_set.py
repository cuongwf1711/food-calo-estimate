# Copyright (C)
# date: 12-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Input Image View Set."""

from rest_framework import permissions, viewsets

from FoodCaloEstimate.estimator.models.my_input_image import MyInputImage
from FoodCaloEstimate.estimator.serializers.input_image_serializer import (
    InputImageSerializer,
)


class InputImageViewSet(viewsets.ModelViewSet):
    """Input Image View Set."""

    queryset = MyInputImage.objects.all()
    serializer_class = InputImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch"]
