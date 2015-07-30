# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 21:07:44 2015

@author: Alexander
"""

from os import chdir
from os import listdir
from time import sleep
from pandas import read_csv
import twitter

from scrapers.random_users import scrape_random_user
from scrapers.retweeters import scrape_retweeter
from scrapers.retweeting_users import scrape_retweeting_user
from scrapers.user_tweets import scrape_user_tweets
from scrapers.timing import ScrapeTimer

from loaders.retweet_list import load_retweet_list



directory = r'C:\Users\Alexander\Documents\Programming\DAT7\DAT7project'
chdir(directory)

#Set timers
retweeter_timer = ScrapeTimer()
ruser_timer = ScrapeTimer()
retuser_timer = ScrapeTimer()
user_tweet_timer = ScrapeTimer()

#15 minute epoch
sec5_in_min15 = 15*60/5
for sec5 in xrange(sec5_in_min15):
    sleep(5)
    #scrape_retweeter(63, retweeter_timer)
    #load_retweet_list(retweeter_timer) #required update for scraping retweeting users
    
    scrape_random_user(6, ruser_timer)
    #scrape_retweeting_user(10,retuser_timer)
    scrape_user_tweets(6, user_tweet_timer)
    #scrape_poster_user
    