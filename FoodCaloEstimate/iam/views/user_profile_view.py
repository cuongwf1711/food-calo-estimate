# Copyright (C)
# date: 22-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""User Profile View."""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from FoodCaloEstimate.iam.models.user_profile import UserProfile
from FoodCaloEstimate.iam.serializers.user_profile_serializer import (
    UserProfileSerializer,
)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User Profile View."""

    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    http_method_names = ["get", "patch"]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)
