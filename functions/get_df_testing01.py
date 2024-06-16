#  vim: set foldmethod=indent foldcolumn=4 :
#!/usr/bin/env python3


import numpy as np
import pandas as pd


def get_df_testing01():

    data = [
        ["8528.05", "Nagle Ave & Ellwood St", 40.748100 + 1e-6, -74.152000],
        ["4077.04", "Smith St & 9 St", 40.684600 + 1e-6, -73.986700],
        ["6676.02", "W 45 St & 8 Ave", 40.936906 + 1e-6, -74.251505],
    ]
    df_trip_biki_station_start = pd.DataFrame(
        data,
        columns=["start_station_id", "start_station_name", "start_lat", "start_lng"],
    )

    data = {
        "STATION": ["USC00283704", "US1NYKN0025", "US1NJPS0015"],
        "LATITUDE": [40.748100, 40.684600, 40.936906],
        "LONGITUDE": [-74.152000, -73.986700, -74.251505],
        "ELEVATION": [7.3, 5.5, 59.1],
    }
    df_weather_unique_stations = pd.DataFrame(data)

    data = {
        "started_at": [
            "2023-01-01",
            "2023-01-01",
            "2023-01-01",
            "2023-12-30",
            "2023-12-30",
        ],
        "rideable_type": [
            "classic_bike",
            "classic_bike",
            "classic_bike",
            "classic_bike",
            "classic_bike",
        ],
        "member_casual": ["member", "member", "member", "member", "member"],
        "start_station_id": ["8528.05", "4077.04", "6676.02", "6676.02", "4077.04"],
        "count": [1, 1, 1, 3, 4],
    }
    df_filtered_grouped = pd.DataFrame(data)

    data = {
        "STATION": [
            "USC00283704",
            "US1NYKN0025",
            "US1NJPS0015",
            "US1NJPS0015",
            "US1NYKN0025",
        ],
        "DATE": ["2023-01-01", "2023-01-01", "2023-01-01", "2023-12-30", "2023-12-30"],
        "AWND": [3.441146, 2.194296, 3.773613, 3.773613, 3.773613],
        "PRCP": [6.65, 0.00, 0.50, 0.30, 0.30],
        "SNOW": [0.0, 0.0, 0.0, 0.1, 0.1],
        "SNWD": [0.0, 0.0, 0.0, 0.1, 0.1],
        "TMAX": [13.3, 30.0, 12.7, 12.7, 9.1],
        "TMIN": [8.050, 10.200, 5.825, 5.825, 5.825],
        "WSF2": [7.488684, 7.429330, 9.698556, 9.698556, 9.698556],
        "WSF5": [9.715263, 10.337248, 12.456059, 10.437248, 9.715263],
        "working_day": [False, False, False, True, True],
        "Monday": [True, True, True, False, False],
        "Tuesday": [False, False, False, False, False],
        "Wednesday": [False, False, False, False, False],
        "Thursday": [False, False, False, False, False],
        "Friday": [False, False, False, False, False],
        "Saturday": [False, False, False, True, True],
        "Sunday": [False, False, False, False, False],
    }

    df_weather_preprocessed = pd.DataFrame(data)

    return (
        df_trip_biki_station_start,
        df_weather_unique_stations,
        df_filtered_grouped,
        df_weather_preprocessed,
    )
