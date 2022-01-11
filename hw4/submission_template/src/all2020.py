import pandas as pd
import numpy as np
import sys

# read previously trimmed data into a dataframe

data = pd.read_csv(sys.argv[1])

# drop any rows with empty fields

data = data.dropna()

# change open & close info to datetime objects

data['open'] = pd.to_datetime(data.open, infer_datetime_format=True)
data['close'] = pd.to_datetime(data.close, infer_datetime_format=True) 

# create time difference column & populate with difference in hours
# & open month only column

data['time'] = data['close'] - data['open']
pd.to_timedelta(data['time'])
data['time'] = data['time'] / np.timedelta64(1, 'h')
data['month'] = pd.DatetimeIndex(data['close']).month

# delete row if time dif is negative or zero

data = data[data.time>0]

# create new dfs for monthly averages

total_av = data.groupby(['month']).time.sum().reset_index()

for i in range(1,10):

    num_cmplts = len(data[data.month == i])
    index = i-1
    total_hrs = total_av.loc[index].at['time']
    total_av.at[index,'time'] = total_hrs/num_cmplts

# output csv

total_av.to_csv('2020_monthly_data.csv')