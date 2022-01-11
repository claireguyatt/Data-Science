# script to clean files containing user posts

import json
from datetime import datetime
import pandas as pd
import pytz
import math
import argparse

# get valid jsons
def get_valid(line):

    # if the input line is valid JSON dict, return it
    try:
        post = json.loads(line)
        return post
        
    # if the input line is an invalid JSON dict, return None
    except: 
        return None

# check for & fix title key
def title_check(post):

    # don't do checks if post already invalid
    if (post == None):
        return None

    title = "title"
    title_text = "title_text"
    # change any 'title_text' to 'title' while keeping as first field
    if title_text in post.keys():
        post = {key if key != 'title_text' else 'title': value for key, value in post.items()}
    # return post if title key is correct
    if title in post.keys():
        return post
    # return None if missing title key
    else:
        return None

# check for & fix time key
def time_check(post):

    # don't do checks if post already invalid
    if (post == None):
        return None
    
    # only do checks if there's a createdAt field
    createdAt = "createdAt"
    if (createdAt in post):
        try:
            created = post[createdAt]
            # create a datetime object from the createdAt field
            dt = datetime.strptime(created, "%Y-%m-%dT%H:%M:%S%z")
            # convert to UTC time
            dt_utc = dt.astimezone(pytz.utc)
            # change createdAt field to updated UTC time & return post
            created = datetime.strftime(dt_utc, "%Y-%m-%dT%H:%M:%S%z")
            post[createdAt] = created
        except:
            # return None if missing key or invalid datetime or post already None
            return None
    return post

# check for author
def author_check(post):

    # don't do checks if post already invalid
    if (post == None):
        return None

    # only do checks if there's an author field
    author = "author"
    if (author in post):
        if (post[author] == "N/A" or post[author] == "" or post[author] == None or post[author] == "null" or post[author] == "empty"):
            return None
    # if no author field or author is valid return original
    return post

# check for total_count
def count_check(post):

    # don't do checks if post already invalid
    if (post == None):
        return None

    # only do checks if there's a count field
    count = "total_count"
    if (count in post):
        # return post only if count field can be typecast to an int
        try:
            num = post[count]
            # if already an int return post (unless neg)
            if (type(num) is int):
                if (num < 0):
                    return None
                else:
                    pass
            # if a string, make float and round down then turn to int
            elif (type(num) is str or type(num) is float):
                num = float(num)
                math.floor(num)
                num = int(num)
                post[count] = num
            # return None if it's not one of the 3 types
            else:
                return None
            return post
        # return None if can't be typecast
        except:
            return None
    # return post if there is no count field
    else:
        return post

def tags_check(post):

    # don't do checks if post already invalid
    if (post == None):
        return None
    
    # do checks only if tag field is present
    tags = "tags"
    if (tags in post):
        for tag in post[tags]:
            # split tag into indv words
            indv_words = tag.split()
            # add all indv words to tags
            post[tags] = post[tags] + indv_words
            # remove the unsplit tags
            post[tags].remove(tag)
    
    return post

# write valid jsons to clean file
def write_valid(post, output):
    with open(output, 'a') as outfile:
        if (post != None):
            json_obj = json.dumps(post)
            outfile.write(json_obj + '\n')

def main():

    # use argparse to get input / output files
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help = "input filename")
    parser.add_argument("-o", help = "output filename")
    args = parser.parse_args()
    input = args.i
    output = args.o

    # erase contents of old clean file
    open(output, 'w').close()

    # loop through input file of json dicts & write them to a clean file
    # if they're valid
    with open(input, 'r') as a_file:
        for line in a_file:
            post = get_valid(line)
            post = title_check(post)
            post = time_check(post)
            post = author_check(post)
            post = count_check(post)
            post = tags_check(post)
            write_valid(post, output)

if __name__ == '__main__':
    main()