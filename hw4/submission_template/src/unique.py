import pandas as pd
  
# read data into dataframe
# data has already been trimmed --> only includes open, close, & ZIP + no empty ZIP cells

data = pd.read_csv("data.csv")

# print distinct ZIPs

x = data['ZIP'].unique()

y = pd.Series(x)

y.to_csv('ZIPs_only.csv', header=None, Index=None)


