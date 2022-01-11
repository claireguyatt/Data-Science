import pandas as pd
import sys

# read the data into a pandas dataframe (only first 10,000 tweets)

header_list = ['1','open','close','4','5','6','7','8','ZIP','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42']
data = pd.read_csv(sys.argv[1], names=header_list, dtype={'ZIP':object}, low_memory=False)

# refine csv to only include required columns & name them

data = data[['open', 'close', 'ZIP']]

# output csv

data.to_csv('data.csv', index=False)
