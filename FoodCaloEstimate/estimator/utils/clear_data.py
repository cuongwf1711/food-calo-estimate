# Copyright (C)
# date: 16-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Clear Data."""


def clear_data(*variables):
    """Clear data."""
    import gc

    import torch

    for t in variables:
        try:
            del t
        except:
            pass

    gc.collect()

    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.reset_accumulated_memory_stats()
