# Copyright (C)
# date: 18-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Custom Decorator."""

import time
from functools import wraps

GREEN = "\033[92m"
RESET = "\033[0m"


def time_measure(func):
    """Decorator to measure the execution time of a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper function."""
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"{GREEN}[TIMING] {func.__qualname__} took {duration:.4f}s{RESET}")
        return result

    return wrapper
