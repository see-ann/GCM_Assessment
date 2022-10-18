#!/usr/bin/env python

#-----------------------------------------------------------------------
# write_csv.py
# Author: Sean Wang
#-----------------------------------------------------------------------

import csv
from tweets_lookup import get_rows
import argparse



def parse_args():
    parser = argparse.ArgumentParser(description='''Get recent tweets 
    by Twitter username''')
    parser.add_argument('-u', metavar="username", help='''Twitter 
    username in the form @username (ie. @KingJames)''')
    parser.add_argument('-e', metavar="edit", choices=['w', 'a'], 
    help='''Overwrite  or add to existing csv file. w for 
    overwrite and a to add.''')
    

    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    username = args.u
    edit = args.e
    rows = get_rows(username)


    # csv header
    fieldnames = ['Twitter Username', 'Tweet', 'Number of Hashtags']

    with open('tweets.csv', edit, encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)




if __name__ == "__main__":
    main()