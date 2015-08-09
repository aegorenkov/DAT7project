# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 15:17:41 2015

@author: Alexander
"""
#Imports
from os import chdir
from random import randrange
from bs4 import BeautifulSoup
from pandas import Dataframe
import csv
directory = r'C:\Users\Alexander\Documents\Programming\DAT7\DAT7project\twitter_search\2'
chdir(directory)

#Helper classes and functions
class SearchStatus(list):
    def __init__(self, tweet_id, user_id, time_stamp, text, retweet_count, 
                 favorite_count):
         self.tweet_id = tweet_id
         self.user_id = user_id
         self.time_stamp = time_stamp
         self.text = text
         self.retweet_count = retweet_count
         self.favorite_count = favorite_count
                     
    def save(self, csvwriter):
        csvwriter.writerow([
            self.tweet_id, 
            self.user_id, 
            self.time_stamp, 
            unicode(self.text).encode('utf8'), 
            self.retweet_count,
            self.favorite_count])

class PersonalVictoryLoader(object):
    
    def __init__(self):
        self._personal_victories = DataFrame()
        
    @staticmethod
    def get_json_file(filename, directory):
        """Returns single line json data as string from json files"""
        with open(directory + '/' + filename, 'r') as json_file:
            json_data = json_file.read()
            json_file.close()
        return json_data
    
    @property
    def personal_vitories(self):
        return self._personal_victories

def extract_tweet_text(tweet):
    """
    Extract text line from html 
    tries multiple class labels to find correct text
    """
    try:
        class_label = "TweetTextSize js-tweet-text tweet-text"
        text = tweet.find(name='p', 
                          attrs={'class': class_label}).text
    except AttributeError:
        pass
    
    try:
        class_label = "TweetTextSize js-tweet-text tweet-text tweet-text-rtl"
        text = tweet.find(name='p', 
                          attrs={'class': class_label}).text
    except AttributeError:
        pass

    return text
    
def extract_retweet_count(s):
    output = s.find(name='span', 
           attrs={'class':"ProfileTweet-actionCountForAria"}).text.split()[0]
    return int(output)
    
def extract_favorites_count(s):
    output = s.find_all(name='span', 
        attrs={'class':"ProfileTweet-actionCountForAria"})[1].text.split()[0]
    return int(output)

#main
with open('#personalvictory_full.html', 'rU') as f:
    html = f.read()
    
b = BeautifulSoup(html)

idname = 'stream-items-id'
tweet_container = b.find(name="ol", attrs={'id': idname})
tweet_list = tweet_container.find_all(name="li", 
                                      attrs = {'data-item-type':'tweet'})
                                      
directory = r'C:\Users\Alexander\Documents\Programming\DAT7\DAT7project'
chdir(directory)
                                      
personalvictory_csv = csv.writer(open(directory + '\\data\\personalvictory.csv', 'wb'))
personalvictory_csv.writerow([
    'tweet_id', 
    'user_id', 
    'time_stamp', 
    'text', 
    'retweet_count',
    'favorite_count'])

for tweet in tweet_list:
    status = SearchStatus(
        tweet_id = tweet.find(name='div')['data-item-id'], 
        user_id = tweet.find(name='div')['data-user-id'], 
        time_stamp = tweet.find(name='span',
                                attrs= {'class':'_timestamp js-short-timestamp '})['data-time'],
        text = extract_tweet_text(tweet),
        retweet_count = extract_retweet_count(tweet),
        favorite_count = extract_favorites_count(tweet))
    status.save(personalvictory_csv)

