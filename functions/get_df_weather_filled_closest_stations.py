#  vim: set foldmethod=indent foldcolumn=4 :
#!/usr/bin/env python3

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

# make it explicit that import is from current directory of current script, not from home folder of main script (or notebook)
#  from .haversine01 import main as haversine01
#  instead of
#  from  haversine01 import main as haversine01
try:
    from .haversine01 import main as haversine01
except ImportError:
    from haversine01 import (
        main as haversine01,
    )  # run current script from current directory


def find_closest_stations(station, all_stations, n):
    distances = all_stations.apply(
        lambda row: haversine01(
            station["LATITUDE"], station["LONGITUDE"], row["LATITUDE"], row["LONGITUDE"]
        ),
        axis=1,
    )
    all_stations_copy = all_stations.copy()
    all_stations_copy["DISTANCE"] = distances.values
    closest_indices = distances.argsort().iloc[:n]
    return all_stations_copy.iloc[closest_indices]


def main(
    df_weather,
    columns_to_fill,
    n=10,
    m=20,
    weight_by_distance=False,
    closest_stations_list=None,
):

    df_weather_filled = df_weather.copy()

    closest_n_dict, closest_m_dict = dict(), dict()

    if closest_stations_list is None:
        closest_stations_list = df_weather_filled["STATION"].unique()

    # Iterate over each ("DATE", "STATION") pair with missing column values
    for column in columns_to_fill:
        for index, row in df_weather[df_weather[column].isnull()].iterrows():
            date = row["DATE"]
            station = row["STATION"]

            # Get all stations except the current one
            other_stations = df_weather[
                (df_weather["DATE"] == date)
                & (df_weather["STATION"] != station)
                & (df_weather["STATION"].isin(closest_stations_list))
            ]

            # Find n closest stations
            if station not in closest_n_dict:  # calculate
                closest_n = find_closest_stations(row, other_stations, n)
                closest_n_dict[station] = closest_n
            else:  # return
                closest_n = closest_n_dict[station]

            # Check if at least n/2 closest stations have column values for that day
            num_closest_with_prcp = closest_n[column].notnull().sum()
            if num_closest_with_prcp >= n / 2:
                if not weight_by_distance:
                    # Calculate the average of non-null column values for the n closest stations
                    avg_prcp = closest_n[column].mean()
                else:
                    # weighted average based on the distance of closest stations
                    distances = closest_n["DISTANCE"]
                    avg_prcp = np.average(
                        closest_n[column], weights=1 / (distances + 1)
                    )
            else:
                # Find m closest stations
                if station not in closest_m_dict:  # calculate
                    closest_m = find_closest_stations(row, other_stations, m)
                    closest_m_dict[station] = closest_m
                else:  # return
                    closest_m = closest_m_dict[station]

                if not weight_by_distance:
                    # Calculate the average of non-null column values for the m closest stations
                    avg_prcp = closest_m[column].mean()
                else:
                    # weighted average based on the distance of closest stations
                    distances = closest_m["DISTANCE"]
                    avg_prcp = np.average(
                        closest_m[column], weights=1 / (distances + 1)
                    )

            # Update the missing column value with the calculated average
            df_weather_filled.at[index, column] = avg_prcp

    return df_weather_filled


if __name__ == "__main__":

    # Mock data
    data = {
        "STATION": [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
        ],  # at least 11, to find 10 closest ones
        "DATE": ["2024-01-01"] * 11,
        "LATITUDE": [41.0, 40.0, 41.0, 42.0, 39.5, 41.5, 40.2, 41.8, 39.7, 40.3, 42.5],
        "LONGITUDE": [
            -75.0,
            -75.0,
            -74.0,
            -73.0,
            -75.5,
            -73.5,
            -74.2,
            -74.8,
            -75.7,
            -73.3,
            -72.5,
        ],
        "PRCP": [
            1.0,
            1.0,
            1.1,
            1.2,
            np.nan,
            0.5,
            0.9,
            1,
            0.2,
            1.5,
            np.nan,
        ],  # Some missing values
        "SNOW": [
            1.0,
            1.0,
            1.1,
            1.2,
            np.nan,
            0.5,
            0.9,
            1,
            0.2,
            1.5,
            np.nan,
        ],  # Some missing values
    }

    # Create DataFrame
    df_weather = pd.DataFrame(data)

    #  df_weather = pd.read_csv('../databases/weather_NOAAA_DailySummaries_230101_231231.csv', sep=',', index_col=False) # year 2023

    # Columns to fill
    columns_to_fill = ["PRCP", "SNOW"]

    # Test the function
    if 1:
        result = main(df_weather, columns_to_fill)
    else:
        result = main(df_weather, columns_to_fill, 4, 6)
    result = main(df_weather, columns_to_fill, n=2, m=4, weight_by_distance=True)
    print(result)
