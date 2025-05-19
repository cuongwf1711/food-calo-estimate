# Copyright (C)
# date: 18-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Custom Decorator."""

import time
from functools import wraps


def time_measure(func):
    """Decorator to measure the execution time of a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper function."""
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"[TIMING] {func.__qualname__} took {duration:.4f}s")
        return result

    return wrapper
