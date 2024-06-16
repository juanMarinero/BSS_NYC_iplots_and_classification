#  vim: set foldmethod=indent foldcolumn=4 :
#!/usr/bin/env python3


def format_float(val, precision=3):
    """float format"""
    if isinstance(val, float):
        return "{:.{}f}".format(val, precision)
    return val
