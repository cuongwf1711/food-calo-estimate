# Copyright (C)
# date: 18-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Custom Decorator."""

from functools import wraps
import time

def time_measure(func):
    """Decorator to measure the execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper function."""
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"[TIMING] {func.__name__} took {duration:.4f}s")
        return result
    return wrapper
