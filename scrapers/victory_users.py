# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 19:14:48 2015

@author: Alexander
"""

from os import chdir
from os import listdir
from pandas import read_csv
import twitter
from random import randrange

directory = r'C:\Users\Alexander\Documents\Programming\DAT7\DAT7project'
chdir(directory)

class TwitterUserCache(object):
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
        cached_users = (f.split('.')[0] for f in files)
        user_lookup = dict()
        for user_id in cached_users:
            user_key = str(user_id)
            user_lookup[user_key] = True
        self._users = user_lookup
    
    def has_user(self, user_id):
        '''Determines whether a user id is in the cache'''
        user_key = str(user_id)
        return self._users.get(user_key, False)

class TwitterUser(object):
    
    def __init__(self, user_id, cache):
        self.user_id = str(user_id)
        self._cache = cache
        
    def user_cached(self):
        self._cache.load_cache()
        return self._cache.has_user(self.user_id)
        
    def load(self):
        if not self.user_cached():
            try:
                user = api.GetUser(user_id=self.user_id, include_entities=True)
                print user
                self._json = user.AsJsonString()
                return True
            except twitter.TwitterError:
                self._json = '{"message": "This id is not associated with a user"}'
                return False
        
    def save(self):
        if not self.user_cached():
            file_name = self._cache.cache_directory + self.user_id + '.json'      
            with open(file_name, 'w') as json_file:
                json_file.write(self._json)
            json_file.close()
            return True
            
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

def scrape_victory_user(rate, timer):
    if timer.ready():
        victory_user_cache = TwitterUserCache(directory + r'/victory_users/')
        personal_victories = read_csv(r'data\personalvictory.csv')
        user_ids = [user for user in personal_victories.user_id if not victory_user_cache.has_user(user)]
        
        user = TwitterUser(user_ids[0], random_user_cache)
        user.load()
        user.save()
        timer.set_next_run(rate)
    else:
        pass

