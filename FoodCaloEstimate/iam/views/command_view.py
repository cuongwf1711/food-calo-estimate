# Copyright (C)
# date: 12-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Command View."""

from django.core.management import call_command
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from utils.message_response_utils import get_message_response


@api_view(["POST"])
@authentication_classes([])
def run_command(request):
    """Run a command."""
    command = request.data.get("command")

    if command:
        try:
            call_command(command)
        except Exception as error:
            return Response(
                get_message_response(success=False, message=str(error)),
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            get_message_response(success=True, message="Command executed successfully.")
        )
    return Response(
        get_message_response(success=False, message="Key Error."),
        status=status.HTTP_400_BAD_REQUEST,
    )
