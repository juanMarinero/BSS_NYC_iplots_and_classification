#  vim: set foldmethod=indent foldcolumn=4 :
#!/usr/bin/env python3

import glob
import warnings
import pandas as pd


def get_bike_stations_API(
    arbitrary_date="2020-04-01",
    file_paths=glob.glob("./databases/citibike_stations/*.csv"),
):

    dfs = []
    warnings.filterwarnings(action="ignore")
    for filename in file_paths:
        df = pd.read_csv(filename)

        col_name = "station_status_last_reported"

        # remove rows that are not numeric
        df[col_name] = pd.to_numeric(df[col_name], errors="coerce")
        df = df.dropna(subset=[col_name])

        timestamps = (
            pd.to_datetime(df[col_name], unit="s")
            .dt.tz_localize("UTC")
            .dt.tz_convert("America/New_York")
        )
        df[col_name] = timestamps

        mask = timestamps.dt.date == pd.Timestamp(arbitrary_date).date()
        df = df[mask]  # keep rows where 'mask' is True

        # print(df.info())
        dfs.append(df)

    # Concatenate all DataFrames into a single DataFrame
    df = pd.concat(dfs, ignore_index=True)
    warnings.resetwarnings()

    return df
