"""Get message response utils."""


def get_message_response(success, message, **kwargs):
    """Return a response object with a message."""
    if success:
        return {"success": success, "message": message, **kwargs}

    return {
        "success": success,
        "errors": {
            "other": [message],
        },
    }
