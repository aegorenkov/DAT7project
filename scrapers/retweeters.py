# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 16:42:53 2015

@author: Alexander
"""

from os import chdir
from os import listdir
from time import sleep
from pandas import read_csv
import twitter
import json

directory = r'C:\Users\Alexander\Documents\Programming\DAT7\DAT7project'
chdir(directory)

class RetweetCache(object):
    '''
    Maintains a rudimentary cache 
    to avoid unnecessarily querying the twitter API
    '''
    
    def __init__(self, cache_directory=directory + r'/random_users/'):
        self.cache_directory = cache_directory
        self.load_cache()
    
    def load_cache(self):
        '''Extracts user ids from cache directory'''
        files = listdir(self.cache_directory)
        cached_statuses = (f.split('.')[0] for f in files)
        status_lookup = dict()
        for status_id in cached_statuses:
            status_key = str(status_id)
            status_lookup[status_key] = True
        self._statuses = status_lookup
    
    def has_status(self, status_id):
        '''Determines whether a user id is in the cache'''
        status_key = str(status_id)
        return self._statuses.get(status_key, False)

class RetweetList(object):
    
    def __init__(self, status_id, cache):
        self.status_id = str(status_id)
        self._cache = cache
        
    def status_cached(self):
        self._cache.load_cache()
        return self._cache.has_status(self.status_id)
        
    def load(self):
        if not self.status_cached():
            try:
                retweeters = api.GetRetweeters(self.status_id)
                print retweeters
                self._json = json.dumps(retweeters)
                return True
            except twitter.TwitterError:
                self._json = '{"message": "This id is not associated with a status"}'
                return False
        
    def save(self):
        if not self.status_cached():
            file_name = self._cache.cache_directory + self.status_id + '.json'      
            with open(file_name, 'w') as json_file:
                json_file.write(self._json)
            json_file.close()
            return True

#Scrape list of retweeters
            
with open('keys/consumer_key.txt','r') as f:
    consumer_key = f.read()
    
with open('keys/consumer_secret.txt','r') as f:
    consumer_secret = f.read()
    
with open('keys/access_token_key.txt','r') as f:
    access_token_key = f.read()
    
with open('keys/access_token_secret.txt','r') as f:
    access_token_secret = f.read()

api = twitter.Api(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token_key=access_token_key,
    access_token_secret=access_token_secret,
)

def scrape_retweeter(rate, timer):
    if timer.ready():
        retweeter_cache = RetweetCache(directory + r'/retweeters/')
        #Load status ids
        personal_victories = read_csv(r'data\personalvictory.csv')
        status_ids = list(
            personal_victories.tweet_id[personal_victories.retweet_count > 0])

        #Clear out statuses that are cached
        status_ids = [s for s in status_ids if not retweeter_cache.has_status(s)]
        retweeters = RetweetList(status_ids[0], retweeter_cache )
        retweeters.load()
        retweeters.save() 
        timer.set_next_run(rate)
    else:
        pass