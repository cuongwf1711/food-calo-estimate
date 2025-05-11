# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Forgot Password View."""

from rest_framework.views import APIView

from FoodCaloEstimate.iam.serializers.forgot_password_serializer import (
    ForgotPasswordSerializer,
)
from FoodCaloEstimate.messages.iam_messages import RESET_PASSWORD_SUCCESS
from utils.message_response_utils import get_message_response
from utils.process_general_request import process_general_request


class ForgotPasswordView(APIView):
    """Forgot Password View."""

    authentication_classes = []

    def post(self, request):
        """Post."""
        return process_general_request(
            request,
            ForgotPasswordSerializer,
            response_data=get_message_response(
                success=True,
                message=RESET_PASSWORD_SUCCESS,
            ),
        )
