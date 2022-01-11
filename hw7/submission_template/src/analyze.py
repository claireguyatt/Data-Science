# take input tsv file & output categorical data

import argparse
import json
import pandas as pd

# open tsv and give output
def output_categories(infile, outfile):

    # convert tsv to pandas df
    df = pd.read_csv(infile, sep='\t')

    # get counts of post types
    c = len(df[df['coding'] == 'c'])
    f = len(df[df['coding'] == 'f'])
    r = len(df[df['coding'] == 'r'])
    o = len(df[df['coding'] == 'o'])

    # turn counts into dict
    counts = {'course-related': c, 'food-related': f, 
                'residence-related': r, 'other': o}
    
    # turn dict into json and save or print
    if outfile != None:
        with open(outfile,'w') as f:
            json.dump(counts, f, indent=4)
    else:
        print(json.dumps(counts, indent=4))

def main():
    
    # use argparse to get input / output files
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help = "input file")
    parser.add_argument("-o", help = "output file")
    args = parser.parse_args()
    infile = args.i
    outfile = args.o

    output_categories(infile, outfile)

if __name__ == '__main__':
    main()