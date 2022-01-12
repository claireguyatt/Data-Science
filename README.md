# comp598-2021
All homeworks from Special Topics Data Science course from Fall 2021.

## hw1

Collect, annotate, and analyze the frequency with which troll Tweets mention "Trump" by name.

## hw2

Set up EC2 instance to run on apache webserver on port 8008 & and an instance of the MariaDB database on port 6002.

## hw3

stats.sh: accepts an input csv file containing Tweets and prints out info from the file.
dialog_analysis.py: takes as input a csv file containing dialog from MLP script, computes stats from the file, and outputs a json file containing the stats.

## hw4

Setup Jupyter on EC2 instance and used to trim a large data file.
Created bokeh dashboard with information about response times for complaints through the 311 service by zipcode.

## hw5

clean.py: accepts an input file and produces a cleaned output file.

## hw6

collect.py: collects data from Reddit's API and outputs json file containing the data.
compute_title_lengths.py: accepts an input json file and outputs a json file containing average title lengths.
collect_relationships.py: accepts an input json file containing target celebrities for "Who's Dated Who" webscraping. Fetches relationships for target individuals and outputs json file containing relationship data.

## hw7

collect_newest.py: collects data from subreddits of Reddit APIs and outputs json file containing the data.
extract_to_tsv.py: accepts an input json file of subreddit data and outputs a json file containing a random selection of the posts to a tsv file.
analyze.py: accepts an input json file of subreddit data and outputs json file containing stats from annotated dats. 

## hw8

compile_word_counts.py: accepts an input csv file of MLP script and computes word counts from each pony, outputs json file containing word count data.
compute_pony_lang.py: accepts an input json file containing MLP word count data and outputs json file with highest frequency words for each pony.

## hw9

build_interaction_network.py: accepts as input csv file of MLP dialog, creates model of an MLP interaction network, and returns json file containing network data. 
compute_network_stats.py: accepts as input json file containing network json file and outputs json file containing network stats.
