#  vim: set foldmethod=indent foldcolumn=4 :
#!/usr/bin/env python3

import pandas as pd
import holidays

# Get the day of the week names
day_of_week_names = pd.Series(pd.date_range("2023-01-01", periods=7)).dt.day_name()
day_of_week_int = pd.Series(pd.date_range("2023-01-01", periods=7)).dt.dayofweek
day_of_week_dict = {day: name for day, name in zip(day_of_week_int, day_of_week_names)}


def get_day_of_week_and_working_day(df, date_col="DATE", holiday_col="holiday"):
    df["day_of_week"] = df[date_col].dt.dayofweek

    # {Saturday or Sunday} or Holiday
    df["working_day"] = (df["day_of_week"].isin([5, 6])) | (df[holiday_col])
    df["working_day"] = ~df["working_day"]

    df = df.join(pd.get_dummies(df["day_of_week"]))

    df.drop(columns=["day_of_week"], inplace=True)
    df.rename(columns=day_of_week_dict, inplace=True)

    return df
