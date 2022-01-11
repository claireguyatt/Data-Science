import pandas as pd
import numpy as np
import sys

# read previously trimmed data into a dataframe

data = pd.read_csv('data.csv')

# drop any rows with empty fields

data = data.dropna()

# change open & close info to datetime objects

data['open'] = pd.to_datetime(data.open, infer_datetime_format=True)
data['close'] = pd.to_datetime(data.close, infer_datetime_format=True)

print("hi")

# create time difference column & populate with difference in hours
# & open month only column

data['time'] = data['close'] - data['open']
pd.to_timedelta(data['time'])
data['time'] = data['time'] / np.timedelta64(1, 'h')
data['month'] = pd.DatetimeIndex(data['close']).month

# delete row if time dif is negative or zero

data = data[data.time>0]

# create new column for monthly averages for the zip & populate

ZIP_av = data.groupby(['ZIP', 'month'])[['time']].mean()
Overall_av = data.groupby(['month'])[['time']].mean()

print(ZIP_av)

# output csvs

ZIP_av.to_csv('ZIPs.csv')
Overall_av.to_csv('all.csv')
