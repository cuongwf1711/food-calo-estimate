# Copyright (C)
# date: 21-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from FoodCaloEstimate.iam.models.user_profile import UserProfile
from FoodCaloEstimate.iam.serializers.reference_point_serializer import (
    ReferencePointSerializer,
)


class ReferencePointView(generics.RetrieveUpdateAPIView):
    """Reference Point View."""

    permission_classes = [IsAuthenticated]
    serializer_class = ReferencePointSerializer

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)
