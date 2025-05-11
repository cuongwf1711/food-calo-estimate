# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

from rest_framework import status
from rest_framework.response import Response


def process_general_request(
    request,
    serializer_class,
    instance=None,
    partial=False,
    status_code=status.HTTP_200_OK,
    response_data=None,
):
    """Process general request."""
    serializer = serializer_class(
        instance, data=request.data, context={"request": request}, partial=partial
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(response_data or serializer.data, status=status_code)
