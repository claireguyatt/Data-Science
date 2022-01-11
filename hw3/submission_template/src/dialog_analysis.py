import csv
import json
import sys
import pandas as pd

# get the data file from the command line and read into pandas dataframe
# & make all data lowercase

raw_data = pd.read_csv(sys.argv[3], index_col=False)
for columns in raw_data.columns:
    raw_data[columns] = raw_data[columns].str.lower()

# make new dataframe for final output & list for looping

data = {'pony':["twilight sparkle",'applejack','rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']}
mlps = ['twilight sparkle','applejack','rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']

data_annotated = pd.DataFrame(data)
data_annotated["count"]=""
data_annotated["verbosity"]=""
data_annotated.set_index('pony', drop=True, inplace=True)

# get speech counts & verbosities for each pony & input to dataframe

loop = 0
for character in mlps:

    speech_acts = len(raw_data[raw_data.pony == character])
    data_annotated.at[character, 'count'] = speech_acts
    verbosity = speech_acts/(len(raw_data) - 1)
    verbosity = round(verbosity, 3)
    data_annotated.at[character, 'verbosity'] = verbosity
    loop = loop + 1

# convert dataframe into json format & save to current folder

data_annotated.to_json(path_or_buf=sys.argv[2], orient="columns", indent=4)


    






