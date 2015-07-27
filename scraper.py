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
from scrape_random_users import scrape_random_user
from scrape_retweeters import scrape_retweeter
from timing import ScrapeTimer

directory = r'C:\Users\Alexander\Documents\Programming\DAT7\DAT7project'
chdir(directory)


#connect_to_twitter()


#Set timers
ruser_timer = ScrapeTimer()
retweeter_timer = ScrapeTimer()

#15 minute epoch

sec5_in_min15 = 15*60/5
for sec5 in xrange(sec5_in_min15):
    sleep(5)
    scrape_random_user(6, ruser_timer)
    scrape_retweeter(63, retweeter_timer )
    
    