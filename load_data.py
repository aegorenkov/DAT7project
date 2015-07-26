# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 18:16:00 2015

@author: Alexander
"""

import json
import csv
from os import chdir
from os import listdir

directory = u'C:\\Users\\Alexander\\Documents\\Programming\\DAT7\\personalvictory_full'
chdir(directory)

def get_user_data(user_file, directory):
    """Loads scraped json files from specified directory"""
    with open(directory + user_file, 'r') as f:
        random_user = json.loads(f.read())
    f.close()
    return random_user

user_files = listdir(directory + r'/random_users')
random_user_csv = csv.writer(open(directory + '\\data\\random_user.csv', 'wb+'))
random_user_csv.writerow([
    'created_at', 
    'favourites_count', 
    'followers_count', 
    'friends_count', 
    'geo_enabled',
    'id',
    'lang',
    'location',
    'profile_background_color',
    'status_created_at',
    'status_favorited',
    'status_hashtags',
    'status_id',
    'status_lang',
    'status_retweet_count',
    'status_retweeted',
    'status_text',
    'statuses_count',
    'time_zone',
    'utc_offset'])

def write_row(random_user, random_user_csv):
    random_user_csv.writerow([
        random_user.get('created_at', 0),
        random_user.get('favourites_count', 0),
        random_user.get('followers_count', 0),
        random_user.get('friends_count', 0),
        unicode(random_user.get('geo_enabled', 'False')).encode('utf8'),
        unicode(random_user.get('id', 'NA')).encode('utf8'),
        unicode(random_user.get('lang', 'NA')).encode('utf8'),
        unicode(random_user.get('location', 'NA')).encode('utf8'),
        unicode(random_user.get('profile_background_color', 'NA')).encode('utf8'),
        unicode(random_user.get('status', dict()).get('created_at', 'NA')).encode('utf8'),
        unicode(random_user.get('status', dict()).get('favorited', 'NA')).encode('utf8'),
        unicode(random_user.get('status', dict()).get('hashtags', 'NA')).encode('utf8'),
        unicode(random_user.get('status', dict()).get('id', 'NA')).encode('utf8'),
        unicode(random_user.get('status', dict()).get('lang', 'NA')).encode('utf8'),
        random_user.get('status', dict()).get('retweet_count', 0),
        unicode(random_user.get('status', dict()).get('retweeted', 'False')).encode('utf8'),
        random_user.get('status', dict()).get('text', 'NA').encode('utf8'),
        random_user.get('statuses_count', 0),
        unicode(random_user.get('time_zone', 'NA')).encode('utf8'),
        unicode(random_user.get('utc_offset', 'NA')).encode('utf8')])
    
for user_file in user_files:
    random_user = get_user_data(user_file, directory + '\\random_users\\')
    if not random_user.has_key('message'):
        write_row(random_user, random_user_csv)
        
user_files = listdir(directory + r'/victory_users')
random_user_csv = csv.writer(open(directory + '\\data\\victory_user.csv', 'wb+'))
random_user_csv.writerow([
    'created_at', 
    'favourites_count', 
    'followers_count', 
    'friends_count', 
    'geo_enabled',
    'id',
    'lang',
    'location',
    'profile_background_color',
    'status_created_at',
    'status_favorited',
    'status_hashtags',
    'status_id',
    'status_lang',
    'status_retweet_count',
    'status_retweeted',
    'status_text',
    'statuses_count',
    'time_zone',
    'utc_offset'])

for user_file in user_files:
    random_user = get_user_data(user_file, directory + '\\victory_users\\')
    if not random_user.has_key('message'):
        write_row(random_user, random_user_csv)
