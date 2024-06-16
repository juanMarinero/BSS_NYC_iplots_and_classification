#  vim: set foldmethod=indent foldcolumn=4 :
#!/usr/bin/env python3

# https://stackoverflow.com/a/70931999/9391770

import numpy as np
import pandas as pd
from pandas.io.formats.info import DataFrameInfo
from IPython.display import display, HTML


# make it explicit that import is from current directory of current script, not from home folder of main script (or notebook)
#  from .haversine01 import main as haversine01
#  instead of
#  from  haversine01 import main as haversine01
try:
    from .hideVals import hideVals
    from .format_float import format_float
    from .generate_random_color import generate_random_color
except ImportError:
    # run current script from current directory
    from hideVals import hideVals
    from format_float import format_float
    from generate_random_color import generate_random_color


def get_df_info(
    df, column_definitions=None, threshold=0  # arbitrary minimum of data 0%
):

    info = DataFrameInfo(data=df)
    infodf = pd.DataFrame(
        {
            "Column": info.ids,
            "Non-Null Count": info.non_null_counts,
            "Dtype": info.dtypes,
        }
    )

    if column_definitions is not None:
        infodf["Description"] = infodf["Column"].map(column_definitions)

    rows = len(df)
    threshold = rows * threshold / 100

    filtered_infodf = infodf[infodf["Non-Null Count"] > threshold].copy()
    percentage = (infodf["Non-Null Count"] / rows) * 100
    filtered_infodf.insert(
        filtered_infodf.columns.get_loc("Non-Null Count") + 1, "Percentage", percentage
    )

    filtered_infodf_style = (
        filtered_infodf.sort_values(by="Non-Null Count", ascending=False)
        .style.hide(axis="index")
        .bar(subset=["Non-Null Count", "Percentage"], color="skyblue")
        .map(generate_random_color, subset=["Dtype"])
        .map(**dict(func=hideVals))
        .set_properties(**{"text-align": "left"})
        .format({"Percentage": "{:.1f} %"})
    )

    return filtered_infodf, filtered_infodf_style
