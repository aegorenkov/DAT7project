# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 20:46:39 2015

@author: Alexander
"""

from os import chdir
from os import listdir
import twitter
import json
import csv

directory = r'C:\Users\Alexander\Documents\Programming\DAT7\DAT7project'
chdir(directory)

def get_json_data(filename, directory):
    with open(directory + '/' + filename, 'r') as f:
        json_data = json.loads(f.read())
    f.close()
    return json_data
    
def load_retweet_list():
    status_retweeters_json = listdir(directory + r'/retweeters')

    retweeter_list = []
    for status in status_retweeters_json:
        retweeters = get_json_data(status, directory + r'/retweeters')
        for retweeter in retweeters:
            retweeter_list.append(retweeter)   
        
        retweet_file = csv.writer(open(directory + '\\data\\retweeter_list.csv', 'wb'))
        retweet_file.writerow('user_id')

    for retweeter in retweeter_list:
        retweet_file.writerow(retweeter_list)