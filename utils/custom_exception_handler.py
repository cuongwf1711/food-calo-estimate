# Copyright (C)
# date: 09-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Exception handler for the project."""

from django.db import connection, transaction
from django.http.response import Http404
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from utils.message_response_utils import get_message_response


def custom_exception_handler(exc, context):
    """Custom exception handler to return a JSON response."""
    set_rollback()
    if isinstance(exc, exceptions.ValidationError):
        data = {"success": False, "errors": exc.detail}
        return Response(data, status=exc.status_code)

    if isinstance(
        exc,
        (
            Http404,
            exceptions.Throttled,
            exceptions.NotAuthenticated,
            exceptions.AuthenticationFailed,
        ),
    ):
        return Response(
            get_message_response(success=False, message=str(exc)),
            status=exc.status_code,
        )

    print(exc)
    print(type(exc))

    return exception_handler(exc, context)


def set_rollback():
    """
    set_rollback https://github.com/encode/django-rest-framework/pull/5591/files
    """
    atomic_requests = connection.settings_dict.get("ATOMIC_REQUESTS", False)
    if atomic_requests and connection.in_atomic_block:
        transaction.set_rollback(True)
