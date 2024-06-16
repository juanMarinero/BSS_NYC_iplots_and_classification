#  vim: set foldmethod=indent foldcolumn=4 :
#!/usr/bin/env python3

import pandas as pd


def hideVals(val):
    """
    Takes a scalar and returns an empty string if it is NaN,
    the original value otherwise.
    """
    # print("'",val,"'", val==np.NaN, val==" nan ", pd.isna(val))

    # error because applymap modifies CSS properties, not values to show
    # return '' if pd.isna(val) else val

    return "color:white;background-color:white" if pd.isna(val) else ""
