# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 12:22:06 2015

@author: Alexander
"""


from os import chdir
from os import listdir
from time import sleep
directory = u'C:\\Users\\Alexander\\Documents\\Programming\\DAT7\\personalvictory_full'
chdir(directory)

with open('keys/consumer_key.txt','r') as f:
    consumer_key = f.read()
    
with open('keys/consumer_secret.txt','r') as f:
    consumer_secret = f.read()
    
with open('keys/access_token_key.txt','r') as f:
    access_token_key = f.read()
    
with open('keys/access_token_secret.txt','r') as f:
    access_token_secret = f.read()

import twitter
api = twitter.Api(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token_key=access_token_key,
    access_token_secret=access_token_secret,
)

print api.VerifyCredentials()


def load_user(user_id):    
    user = api.GetUser(user_id=user_id, include_entities=True)
    
20480261    
2042870261    

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

rand_users = []
with open('user_ids100', 'rU') as random_users_file:
    for line in random_users_file.readlines():
        rand_users.append(line.strip())
random_users_file.close()


victory_users = []
with open('victory_user_ids100', 'rU') as victory_users_file:
    for line in victory_users_file.readlines():
        victory_users.append(line.strip())
victory_users_file.close()

        
random_user_cache = TwitterUserCache(directory + r'/random_users/')
for user_id in rand_users[200:]:
    sleep(2)
    user = TwitterUser(user_id, random_user_cache)
    user.load()
    user.save()
    
    
victory_user_cache = TwitterUserCache(directory + r'/victory_users/')
for user_id in victory_users:
    sleep(2)
    user = TwitterUser(user_id, victory_user_cache)
    user.load()
    user.save()