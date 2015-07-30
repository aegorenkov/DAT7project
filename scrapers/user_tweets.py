# -*- coding: utf-8 -*-
"""
Scrape 200 most recent statuses posted by a given Twitter user
"""

from os import chdir
from os import listdir
from pandas import read_csv
import twitter
import pandas as pd
import itertools

directory = r'C:\Users\Alexander\Documents\Programming\DAT7\DAT7project'
chdir(directory)

class UserTimelineCache(object):
    '''
    Maintains a rudimentary cache 
    to avoid unnecessarily querying the twitter API
    '''
    
    def __init__(self, cache_directory=directory + r'/user_timelines/'):
        self.cache_directory = cache_directory
        self.load_cache()
    
    def load_cache(self):
        '''Extracts user ids from cache directory'''
        files = listdir(self.cache_directory)
        cached_users = (f.split('_')[0] for f in files)
        user_lookup = dict()
        for user_id in cached_users:
            user_key = str(user_id)
            user_lookup[user_key] = True
        self._users = user_lookup
    
    def has_user(self, user_id):
        '''Determines whether a user id is in the cache'''
        user_key = str(user_id)
        return self._users.get(user_key, False)

class UserTimeline(object):
    
    def __init__(self, user_id, cache):
        self.user_id = str(user_id)
        self._cache = cache
        
    def user_cached(self):
        self._cache.load_cache()
        return self._cache.has_user(self.user_id)
        
    def load(self):
        if not self.user_cached():
            try:
                user_timeline = api.GetUserTimeline(user_id=self.user_id, count=200)
                print user_timeline
                if not user_timeline:
                    self._json = dict(('NA', 'NA'))
                    return False
                #Make this a dictionary with json values and status key
                keys = [status.GetId() for status in user_timeline]
                values = [u.AsJsonString() for u in user_timeline]
                self._json = dict(zip(keys, values))
                return True
            except twitter.TwitterError:
                self._json = '{"message": "This id is not associated with a user"}'
                return False
        
    def save(self):
        if not self.user_cached():
            if type(self._json) != str:
                for key in self._json.iterkeys():
                    file_name = self._cache.cache_directory + self.user_id + '_' + str(key) +  '.json'      
                    with open(file_name, 'w') as json_file:
                        json_file.write(self._json[key])
                        json_file.close()
            else:
                file_name = self._cache.cache_directory + self.user_id + '_' + 'fail' +  '.json'      
                with open(file_name, 'w') as json_file:
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

def scrape_user_tweets(rate, timer):
    if timer.ready():
        user_timeline_cache = UserTimelineCache(directory + r'/user_timelines/')
        #Get user list
        personal_victory = pd.read_csv(r'data\personalvictory.csv')
        random_user = pd.read_csv(r'data\random_user.csv')
        retweet_list = pd.read_csv(r'data\retweeter_list.csv')
        #users_pv = [s for s in personal_victory.user_id if not user_timeline_cache.has_user(s)]
        users_ru = [s for s in random_user.id if not user_timeline_cache.has_user(s)]
        #users_rl = [s for s in retweet_list.user_id if not user_timeline_cache.has_user(s)]

        #user_list = list(itertools.chain(users_pv, users_ru, users_rl))
        user_list = list(itertools.chain(users_ru))

        if user_list:
            user = UserTimeline(user_list[0], user_timeline_cache)
            user.load()
            user.save()
        timer.set_next_run(rate)
    else:
        pass 
