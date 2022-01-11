# download a bunch of stuff from reddit

import requests
import json
import pandas as pd
import os

# download & save data from input URL
def  get_data(subreddit):

    # personal app & account stuff
    ID = "QLww140vMx0fDn80hXTHmA"
    secret = "y3CB4q_9sz-n2NqSUQ3q5sGJqc-sMA"
    uname = "COMP598_DataAnal"
    pw = "LeoIsSexy123"

    # nrequest OAuth token
    auth = requests.auth.HTTPBasicAuth(ID, secret)

    # login method (username & pw)
    data = {'grant_type': 'password', 'username': uname, 'password': pw}

    # setup header info (give reddit a brief description of app)
    headers = {'User-Agent': 'DataAnalforClass/0.0.1'}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)

    # convert response to JSON and pull access_token value
    TOKEN = res.json()['access_token']

    # add authorization to headers dictionary
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    # while the token is valid (~2 hours) add headers=headers to requests
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    # get & return json using input subreddit
    string  = "https://oauth.reddit.com/r/" + subreddit + "/new.json?limit=100"
    res = requests.get(string, headers=headers)
    return res.json()

# append new json to json file with only children (posts)
def merge_jsons(sample, output_file):
    
    all = []
    for subreddit in sample:
        
        # get data from reddit API & put into json file
        data = get_data(subreddit)
        with open('file.json', 'w') as f:
            json.dump(data, f)
        with open('file.json', 'r') as f:
            data = json.load(f)
        # change into dict and get rid of outter part (so just keep children)
        # and merge into og dict
        temp = data['data']['children']
        all.extend(temp)
    
    # delete temp file
    os.remove('file.json')

    with open(output_file, 'w') as f:
        for d in all:
        # 1 json dict per line (not actual json format)
            f.write(json.dumps(d) + "\n") 
            if d == temp[-1]:
                break

def main():
    
    # sample1 list
    s1_list = ['funny', 'AskReddit', 'gaming', 'aww', 'pics', 'Music', 
            'science', 'worldnews', 'videos', 'todayilearned']
    s1_path = "sample1.json"

    # sample2 list
    s2_list = ['AskReddit', 'memes', 'politics', 'nfl', 'nba','wallstreetbets',
                'teenagers', 'PublicFreakout', 'leagueoflegends', 'unpopularopinion']
    s2_path = "sample2.json"
    
    # get separate sample files based on subscribers/ post#
    merge_jsons(s1_list, s1_path)
    merge_jsons(s2_list, s2_path)

if __name__ == '__main__':
    main()