#  vim: set foldmethod=indent foldcolumn=4 :
#!/usr/bin/env python3


import pandas as pd


def get_X_y(df, count_percentile, x_cols=None):
    if x_cols is None:
        x_cols = list(
            set(df.columns)
            - set(
                ["count", "started_at", "start_station_id", "closest_weather_station"]
            )
        )

    X = df[x_cols].values
    y = count_percentile

    return X, y, x_cols
