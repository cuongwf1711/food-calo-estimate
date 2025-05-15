# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Queue Tasks."""

import logging
import pickle
import random

from celery import group

from FoodCaloEstimate.celery import shared_task
from FoodCaloEstimate.iam.constants.general_constants import TIMEOUT_SERVER


@shared_task
def add_test_queue(x, y):
    import time

    time.sleep(10)
    return random.randint(x, y)


@shared_task
def generic_task_executor(serialized_data):
    """Generic task to execute a function from the specified module."""
    try:
        func, args, kwargs = pickle.loads(serialized_data)
        return func(*args, **kwargs)
    except BaseException as error:
        import traceback

        traceback.print_exc()
        logging.error(f"Error executing function in queue: {error}")


def run_task_in_queue(func, *args, **kwargs):
    """Run a function in the queue."""
    generic_task_executor.delay(pickle.dumps((func, args, kwargs)))


def run_parallel_tasks_in_queue(*tasks):
    groups = group(
        generic_task_executor.s(pickle.dumps((func, args, kwargs)))
        for func, args, kwargs in tasks
    )
    return groups.apply_async().join_native(timeout=TIMEOUT_SERVER)
