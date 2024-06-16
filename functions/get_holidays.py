#  vim: set foldmethod=indent foldcolumn=4 :
#!/usr/bin/env python3

import pandas as pd
import holidays

def get_holidays(dates, years=[2023]):
    """Add the holidays of 2023 in New York as a column of the dataframe 'df'.
    
    Parameters
    ----------
    df_dates: pd.Series
        Series containing datetime objects representing the dates.
    years: list
        List of years to get holidays
    
    Returns
    -------
    list
       'holiday' list indicating if True each date passed.
    """
    
    # Get the holidays for New York in 2023
    ny_holidays = holidays.US(years=years, state='NY')
    
    # Convert dictionary keys (datetime.date objects) to datetime64[ns] objects
    holiday_dates = pd.to_datetime(list(ny_holidays.keys()))
    
    return dates.isin(holiday_dates)
