# Copyright (C)
# date: 09-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

from rest_framework.response import Response
from rest_framework.views import APIView

from FoodCaloEstimate.iam.serializers.sign_up_email_serializer import (
    SignupEmailSerializer,
)
from FoodCaloEstimate.messages.iam_messages import ACCOUNT_SIGN_UP_SUCCESS
from FoodCaloEstimate.queue_tasks import add_test_queue
from utils.message_response_utils import get_message_response
from utils.process_general_request import process_general_request


class SiginUpEmailView(APIView):
    """Sginup view for user registration."""

    authentication_classes = []
    # throttle_rates = {
    #     "get": "1/5s",
    # }

    def get(
        self, request, *args, **kwargs
    ):  # test: {{base_url}}/api/v1/iam/auth/signup
        """Get."""
        add_test_queue.delay(1, 20)
        return Response(123)

    def post(self, request, *args, **kwargs):
        """Handle POST request for signup."""
        return process_general_request(
            request,
            SignupEmailSerializer,
            response_data=get_message_response(
                success=True,
                message=ACCOUNT_SIGN_UP_SUCCESS,
            ),
        )
