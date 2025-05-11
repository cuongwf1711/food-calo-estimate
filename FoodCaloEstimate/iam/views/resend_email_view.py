# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Resend Email View."""

from rest_framework.views import APIView

from FoodCaloEstimate.iam.serializers.resend_email_serializer import (
    ResendEmailSerializer,
)
from FoodCaloEstimate.messages.iam_messages import EMAIL_SENT
from utils.message_response_utils import get_message_response
from utils.process_general_request import process_general_request


class ResendEmailView(APIView):
    """Resend Email View."""

    authentication_classes = []

    def post(self, request, *args, **kwargs):
        """Resend email."""
        return process_general_request(
            request,
            ResendEmailSerializer,
            response_data=get_message_response(
                success=True,
                message=EMAIL_SENT,
            ),
        )
