#!/usr/bin/env python

#-----------------------------------------------------------------------
# user_id_lookup.py
# Author: Sean Wang
#-----------------------------------------------------------------------

import requests
import os

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_url(username):
    # get rid of @ at the start of the username
    username = username[1:]

    return "https://api.twitter.com/2/users/by/username/{}".format(username)


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

def get_user_id(username):
    url = create_url(username)
    json_response = connect_to_endpoint(url, None)
    return json_response["data"]["id"]
