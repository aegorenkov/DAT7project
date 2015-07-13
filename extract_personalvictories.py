# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 18:12:18 2015

@author: Alexander
"""

from os import chdir
from random import randrange

directory = u'C:\\Users\\Alexander\\Documents\\Programming\\DAT7\\personalvictory_full'
chdir(directory)


with open('#personalvictory_full.html', 'rU') as f:
    html = f.read()
    
from bs4 import BeautifulSoup
b = BeautifulSoup(html)

classname = 'js-stream-item stream-item stream-item expanding-stream-item'
b.find_all(name="li")
print test

idname = 'stream-items-id'
tweet_container = b.find(name="ol", attrs={'id': idname})
tweet_list = tweet_container.find_all(name="li", 
                                      attrs = {'data-item-type':'tweet'})


class TwitterList(list):
    def __init__(self, b):
        self.b = b

tweet_list[0]['data-item-id']
tweet_ids = [s['data-item-id'] for s in tweet_list]
victory_user_ids = [int(s.find(name='div')['data-user-id']) for s in tweet_list]

tweet_list[0].find(name='div')['data-screen-name']
tweet_list[0].find(name='div')['data-user-id']
tweet_list[0].find(name='span',
    attrs= {'class':'_timestamp js-short-timestamp js-relative-timestamp'})['data-time']
    
#tweet text
#tweet favorites
<span class="ProfileTweet-actionCountForAria" data-aria-label-part="">1 favorite</span>
tweet_list[0].find_all(name='span', 
    attrs={'class':"ProfileTweet-actionCountForAria"})[1].text.split()[0]
#tweet retweets
<span class="ProfileTweet-actionCountForAria">0 retweets</span>
tweet_list[0].find(name='span', 
    attrs={'class':"ProfileTweet-actionCountForAria"}).text.split()[0]

def extract_retweet_count(s):
    output = s.find(name='span', 
           attrs={'class':"ProfileTweet-actionCountForAria"}).text.split()[0]
    return int(output)
    
def extract_favorites_count(s):
    output = s.find_all(name='span', 
        attrs={'class':"ProfileTweet-actionCountForAria"})[1].text.split()[0]
    return int(output)
    
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