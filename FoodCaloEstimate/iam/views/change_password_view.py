# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Change Password View."""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from FoodCaloEstimate.iam.serializers.change_password_serializer import (
    ChangePasswordSerializer,
)
from FoodCaloEstimate.messages.iam_messages import CHANGE_PASSWORD_SUCCESS
from utils.message_response_utils import get_message_response


class ChangePasswordView(APIView):
    """Change Password View."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Handle POST request to change password."""
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.update(request.user, serializer.validated_data)
        except Exception as error:
            return Response(
                get_message_response(success=False, message=str(error)),
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            get_message_response(success=True, message=CHANGE_PASSWORD_SUCCESS),
        )
