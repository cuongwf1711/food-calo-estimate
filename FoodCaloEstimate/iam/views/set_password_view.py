# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Set Password View."""

from rest_framework.views import APIView

from FoodCaloEstimate.iam.serializers.set_password_serializer import (
    SetPasswordSerializer,
)
from FoodCaloEstimate.messages.iam_messages import ACCOUNT_SET_PASSWORD_SUCCESS
from utils.message_response_utils import get_message_response
from utils.process_general_request import process_general_request


class SetPasswordView(APIView):
    """Set Password View."""

    authentication_classes = []

    def post(self, request, *args, **kwargs):
        """Set password."""
        return process_general_request(
            request,
            SetPasswordSerializer,
            response_data=get_message_response(
                success=True,
                message=ACCOUNT_SET_PASSWORD_SUCCESS,
            ),
        )
