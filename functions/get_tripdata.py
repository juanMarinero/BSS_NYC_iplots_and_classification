#  vim: set foldmethod=indent foldcolumn=4 :
#!/usr/bin/env python3

import numpy as np
import pandas as pd
import glob

# make it explicit that import is from current directory of current script, not from home folder of main script (or notebook)
#  from .haversine01 import main as haversine01
#  instead of
#  from  haversine01 import main as haversine01
try:
    from .dump_or_load import dump_or_load
except ImportError:
    from dump_or_load import (
        main as dump_or_load,
    )  # run current script from current directory

pickle_folder = "./databases/pickle/"

def get_tripdata(file_paths, 
                 filename = pickle_folder + "df_tripdata_2023-01-01_to_2023-05-30.pkl",
                 cols_to_remove = ['ride_id', 'ended_at','end_station_name', 'end_station_id', 'end_lat', 'end_lng']
                 ):


    if 1:
        df = read_csv_files_01(file_paths)
    else:
        df = read_csv_files_02(file_paths, batch_size=2)
    print("Files read done!")

    df.drop(columns=cols_to_remove, inplace=True)


    df_filtered = df.query("start_lat.notna() and start_lng.notna()").copy()

    cols = ['start_station_name', 'start_lat', 'start_lng']
    df_trip_biki_station_start = df_filtered.drop_duplicates(subset='start_station_id', keep='first', inplace=False)\
    [['start_station_id'] + cols]
    df_trip_biki_station_start.set_index('start_station_id', inplace=True) 
    df_trip_biki_station_start.reset_index(inplace=True)


    #  print(file_paths)
    #  print(set(df_filtered["started_at"]))
    df_filtered.drop(columns=cols, inplace=True)

    df_filtered["started_at"] = pd.to_datetime(df_filtered["started_at"], format="%Y-%m-%d %H:%M:%S").dt.floor('D')

    df_filtered = df_filtered.rename(columns={'member_casual': 'member_T_casual_F'})
    df_filtered['member_T_casual_F'] = np.where(df_filtered['member_T_casual_F'] == 'member', True, False)

    df_filtered = df_filtered.join(pd.get_dummies(df_filtered['rideable_type']))
    df_filtered.drop(columns=["rideable_type"], inplace=True)

    df_filtered_grouped = df_filtered.groupby(list(df_filtered.columns)).size().reset_index(name='count')


    files = []
    files.append(filename[:-4]+"_biki_station_start"+filename[-4:])
    files.append(filename[:-4]+"_filtered_grouped"+filename[-4:])

    return [df_trip_biki_station_start, df_filtered_grouped], files

def read_csv_files_01(file_paths):
    dfs = []

    for file_path in file_paths:
        # Read the CSV file into a DataFrame and append it to the list
        df = pd.read_csv(file_path, sep=",", low_memory=False)
        dfs.append(df)
    # Concatenate all DataFrames into a single DataFrame
    df = pd.concat(dfs, ignore_index=True)
    return df

def read_pickle_files_01(file_paths):
    dfs = []

    for file_path in file_paths:
        # Read the pickle file into a DataFrame and append it to the list
        df = dump_or_load(file_path, dump=False)
        dfs.append(df)
    # Concatenate all DataFrames into a single DataFrame
    df = pd.concat(dfs, ignore_index=True)
    return df

def read_csv_files_02(file_paths, batch_size=4):
    dfs = []

    for i in range(0, len(file_paths), batch_size):
        batch_file_paths = file_paths[i:i+batch_size]
        batch_dfs = []

        for file_path in batch_file_paths:
            df = pd.read_csv(file_path, sep=",", low_memory=False)
            batch_dfs.append(df)

        combined_df = pd.concat(batch_dfs, ignore_index=True)
        dfs.append(combined_df)

    # Concatenate all DataFrames into a single DataFrame
    df = pd.concat(dfs, ignore_index=True)
    return df

def byhand(dfs, file_bin):
    mtot=0
    with open(file_bin,'wb') as f:
        for df in dfs:
            m,n =df.shape
            mtot += m
            f.write(df.values.tobytes())
            typ=df.values.dtype
    print("byhand opened!")
    del dfs
    with open(file_bin,'rb') as f:
        buffer=f.read()
        data=np.frombuffer(buffer,dtype=typ).reshape(mtot,n)
        df_all=pd.DataFrame(data=data,columns=list(range(n)))
    os.remove(file_bin)
    print("byhand finnished!")
    return df_all

def main(opt=0):
    files = []
    files.append(pickle_folder + "df_tripdata_2023-01-01_to_2023-04-30.pkl")
    files.append(pickle_folder + "df_tripdata_2023-05-01_to_2023-08-31.pkl")
    files.append(pickle_folder + "df_tripdata_2023-09-01_to_2023-12-31.pkl")

    match opt:
        case 0:
            # Killed cause low memory
            # Use glob to get a list of file paths matching the pattern
            file_paths = glob.glob("./databases/2023-citibike-tripdata/[1-12]*/*.csv")
            filename = pickle_folder + "df_tripdata_2023-01-01_to_2023-12-31.pkl"
        case 1:
            filename = files[0]
            #  file_paths = glob.glob("./databases/2023-citibike-tripdata/1_Jan*/*.csv") # deleteme!!!!
            file_paths = glob.glob("./databases/2023-citibike-tripdata/[1-4]_*/*.csv")
        case 2:
            filename = files[1]
            file_paths = glob.glob("./databases/2023-citibike-tripdata/[5-8]*/*.csv")
        case 3:
            filename = files[2]
            file_paths = glob.glob("./databases/2023-citibike-tripdata/[9]*/*") + glob.glob("./databases/2023-citibike-tripdata/[1][0-2]*/*")
        case 98:
            # ERROR
            dfs = []
            for file in files:
                dfs.append(dump_or_load(file, dump=False))
            df_tripdata = pd.concat(dfs, ignore_index=True)
        case 99:
            # write 1 huge CSV, afterwards run opt=100
            filename_csv = pickle_folder + "df_tripdata_2023-01-01_to_2023-12-31.csv"

            for i, file in enumerate(files):
                df = dump_or_load(file, dump=False)
                df.to_csv(filename_csv, index=False, mode='a' if i>0 else 'w')
                # free memory
                del df
        case 100:
            # Killed cause low memory
            filename = pickle_folder + "df_tripdata_2023-01-01_to_2023-12-31.pkl"
            filename_csv = pickle_folder + "df_tripdata_2023-01-01_to_2023-12-31.csv"
            file_paths = [filename_csv]
        case 101:
            # https://stackoverflow.com/questions/44715393/how-to-concatenate-multiple-pandas-dataframes-without-running-into-memoryerror
            if 0:
                # Killed cause low memory
                filename = pickle_folder + "df_tripdata_2023-01-01_to_2023-12-31.pkl"
                filename_bin = pickle_folder + "df_tripdata_2023-01-01_to_2023-12-31.bin"
            else:
                # Killed cause low memory
                files.pop(0) # remove 1st file to try no get ERROR
                filename = pickle_folder + "df_tripdata_2023-06-01_to_2023-12-31.pkl"
                filename_bin = pickle_folder + "df_tripdata_2023-06-01_to_2023-12-31.bin"
            dfs = []
            for file in files:
                dfs.append(dump_or_load(file, dump=False))
            df_tripdata = byhand(dfs, filename_bin)

    if opt not in [98, 99]:
        dfs, filenames = get_tripdata(file_paths, filename)

    for i, df in enumerate(dfs):
        dump_or_load(filenames[i], var=df, dump=True)

if __name__ == "__main__":
    # Jupyter crash, run from script

    #  (venv) ~/MEGAsync/IT_xopi_UOC_MasterDataScience/03_TFM/code  $  python -m functions.get_tripdata

    if 1:
        main(1)
        main(2)
        main(3)

    # output:
    #  (venv) ~/MEGAsync/IT_xopi_UOC_MasterDataScience/03_TFM/code  $  python -m functions.get_tripdata
    #  Files read done!
    #  Saved  <_io.BufferedWriter name='./databases/pickle/df_tripdata_2023-01-01_to_2023-04-30_biki_station_start.pkl'>
    #  Saved  <_io.BufferedWriter name='./databases/pickle/df_tripdata_2023-01-01_to_2023-04-30_filtered_grouped.pkl'>
    #  Files read done!
    #  Saved  <_io.BufferedWriter name='./databases/pickle/df_tripdata_2023-05-01_to_2023-08-31_biki_station_start.pkl'>
    #  Saved  <_io.BufferedWriter name='./databases/pickle/df_tripdata_2023-05-01_to_2023-08-31_filtered_grouped.pkl'>
    #  Files read done!
    #  Saved  <_io.BufferedWriter name='./databases/pickle/df_tripdata_2023-09-01_to_2023-12-31_biki_station_start.pkl'>
    #  Saved  <_io.BufferedWriter name='./databases/pickle/df_tripdata_2023-09-01_to_2023-12-31_filtered_grouped.pkl'>
    #  (venv) ~/MEGAsync/IT_xopi_UOC_MasterDataScience/03_TFM/code  $
