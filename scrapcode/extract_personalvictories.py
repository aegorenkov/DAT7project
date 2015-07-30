# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 18:12:18 2015

@author: Alexander
"""

from os import chdir
from random import randrange
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser

class SearchStatus(list):
    def __init__(self, tweet_id, user_id, time_stamp, text, retweet_count, 
                 favorite_count):
         self.tweet_id = tweet_id
         self.user_id = user_id
         self.time_stamp = time_stamp
         self.text = text
         self.retweet_count = retweet_count
         self.favorite_count = favorite_count
                     
    def save(self):
        pass

directory = r'C:\Users\Alexander\Documents\Programming\DAT7\DAT7project\twitter_search\2'
chdir(directory)

with open('#personalvictory_full.html', 'rU') as f:
    html = f.read()
    
b = BeautifulSoup(html)

classname = 'js-stream-item stream-item stream-item expanding-stream-item'

idname = 'stream-items-id'
tweet_container = b.find(name="ol", attrs={'id': idname})
tweet_list = tweet_container.find_all(name="li", 
                                      attrs = {'data-item-type':'tweet'})
def extract_retweet_count(s):
    output = s.find(name='span', 
           attrs={'class':"ProfileTweet-actionCountForAria"}).text.split()[0]
    return int(output)
    
def extract_favorites_count(s):
    output = s.find_all(name='span', 
        attrs={'class':"ProfileTweet-actionCountForAria"})[1].text.split()[0]
    return int(output)

status = SearchStatus(
            tweet_id = tweet_list[0]['data-item-id'], 
            user_id = tweet_list[0].find(name='div')['data-user-id'], 
            time_stamp = tweet_list[0].find(name='span',
                attrs= {'class':'_timestamp js-short-timestamp '})['data-time'],
            text = tweet_list[0].find(name='p', 
                attrs={'class':"TweetTextSize js-tweet-text tweet-text"}).text,
            retweet_count = extract_retweet_count(tweet_list[0]),
            favorite_count = extract_favorites_count(tweet_list[0]))

        
tweet_list[0]['data-item-id']
tweet_ids = [s['data-item-id'] for s in tweet_list]
victory_user_ids = [int(s.find(name='div')['data-user-id']) for s in tweet_list]

tweet_list[0].find(name='div')['data-screen-name']
tweet_list[0].find(name='div')['data-user-id']
tweet_list[0].find(name='span',
    attrs= {'class':'_timestamp js-short-timestamp '})['data-time']
    
#tweet text
#tweet favorites
tweet_list[0].find_all(name='span', 
    attrs={'class':"ProfileTweet-actionCountForAria"})[1].text.split()[0]
#tweet retweets
tweet_list[0].find(name='span', 
    attrs={'class':"ProfileTweet-actionCountForAria"}).text.split()[0]

tweet_list[0].find(name='p', 
    attrs={'class':"TweetTextSize js-tweet-text tweet-text"})
    
retweet_count_list = [extract_retweet_count(s) for s in tweet_list]

favorites_count_list = [extract_favorites_count(s) for s in tweet_list]



rand_users = [randrange(min(user_ids), max(user_ids), 1) for s in range(100)]

with open('user_ids100', 'a') as user_file:
    for user in rand_users:
        user_file.write(str(user)+'\n')
user_file.close()

with open('victory_user_ids100', 'w') as user_file:
    for user in victory_user_ids[0:100]:
        user_file.write(str(user)+'\n')
user_file.close()