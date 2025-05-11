def get_message_response(success, message, **kwargs):
    """Return a response object with a message."""
    if success:
        result = {
            "success": success,
            "message": message,
        }

        for key, value in kwargs.items():
            result[key] = value

        return result

    return {
        "success": success,
        "errors": {
            "other": [message],
        },
    }
