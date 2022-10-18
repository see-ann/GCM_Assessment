#!/usr/bin/env python

#-----------------------------------------------------------------------
# tweets_lookup.py
# Author: Sean Wang
#-----------------------------------------------------------------------


import requests
import os
import re
from user_id_lookup import get_user_id

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")



def create_url(id):
    return "https://api.twitter.com/2/users/{}/tweets".format(id)


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

def json_parser(json_response, username):
    rows = []
    for _, data in enumerate(json_response['data']):
        tweet = data['text']
        row = {}
        row["Twitter Username"] = username
        row["Tweet"] = remove_emojis(tweet)
        num_hashtags = 0
        # count number of hashtags
        for _ in re.findall('#(\w+)', tweet):
            num_hashtags+=1
        row["Number of Hashtags"] = num_hashtags
        rows.append(row)
    return rows


def get_rows(username):
    id = get_user_id(username)
    url = create_url(id)
    json_response = connect_to_endpoint(url, None)
    rows = json_parser(json_response, username)
    return rows



