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
        except NameError:
            pass

    # Clear CUDA cache
    torch.cuda.empty_cache()

    # Clear PyTorch cache
    torch.cuda.ipc_collect()

    # Clear Python garbage collector
    gc.collect()
