# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Queue Tasks."""

import base64
import logging
import pickle
import random

from celery import shared_task


@shared_task
def add_test_queue(x, y):
    import time

    time.sleep(10)
    return random.randint(x, y)


@shared_task
def generic_task_executor(serialized_data):
    """Generic task to execute a function from the specified module."""
    try:
        func, args, kwargs = pickle.loads(base64.b64decode(serialized_data))
        func(*args, **kwargs)
    except Exception as error:
        import traceback

        traceback.print_exc()
        logging.error(f"Error executing function in queue: {error}")


def run_task_in_queue(func, *args, **kwargs):
    """Run a function in the queue."""
    generic_task_executor.delay(
        base64.b64encode(pickle.dumps((func, args, kwargs))).decode("utf-8")
    )
