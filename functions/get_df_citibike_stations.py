#  vim: set foldmethod=indent foldcolumn=4 :
#!/usr/bin/env python3

#  https://www.kaggle.com/datasets/rosenthal/citi-bike-stations?resource=download

import pandas as pd


def read_csv(filename: str) -> pd.DataFrame:
    """
    Read DataFrame from a CSV file ``filename`` and convert to a
    preferred schema.
    """
    df = pd.read_csv(
        filename,
        sep=",",
        na_values="\\N",
        dtype={
            "station_id": str,
            # Use Pandas Int16 dtype to allow for nullable integers
            "num_bikes_available": "Int16",
            "num_ebikes_available": "Int16",
            "num_bikes_disabled": "Int16",
            "num_docks_available": "Int16",
            "num_docks_disabled": "Int16",
            "is_installed": "Int16",
            "is_renting": "Int16",
            "is_returning": "Int16",
            "station_status_last_reported": "Int64",
            "station_name": str,
            "lat": float,
            "lon": float,
            "region_id": str,
            "capacity": "Int16",
            # Use pandas boolean dtype to allow for nullable booleans
            "has_kiosk": "boolean",
            "station_information_last_updated": "Int64",
            "missing_station_information": "boolean",
        },
    )
    # Read in timestamps as UNIX/POSIX epochs but then convert to the local
    # bike share timezone.
    df["station_status_last_reported"] = pd.to_datetime(
        df["station_status_last_reported"], unit="s", origin="unix", utc=True
    ).dt.tz_convert("US/Eastern")

    df["station_information_last_updated"] = pd.to_datetime(
        df["station_information_last_updated"], unit="s", origin="unix", utc=True
    ).dt.tz_convert("US/Eastern")
    return df
