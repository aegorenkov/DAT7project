# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 14:09:37 2015

@author: Alexander
"""

from os import chdir
from os import listdir
import json
import csv

directory = r'C:\Users\Alexander\Documents\Programming\DAT7\DAT7project'
chdir(directory)

def get_json_data(filename, directory):
    with open(directory + '/' + filename, 'r') as f:
        json_data = json.loads(f.read())
    f.close()
    return json_data
    
data = dict()
user_timelines_json = listdir(directory + r'/user_timelines')
for timeline in user_timelines_json:
    if timeline.split('_')[1].startswith('fail'):
        continue
    if timeline.split('_')[1].startswith('N'):
        continue
    line = get_json_data(timeline, directory + r'/user_timelines')
    data_entry = data.get(line['user']['id'], False)
    if data_entry:
        data_entry.append(line['text'])
    else:
        data[line['user']['id']] = [line['text']]
    
for key in data.iterkeys():
    data[key] = ''.join(data[key])
    
tweetdeck_file = csv.writer(open(directory + '\\data\\tweetdeck.csv', 'wb'))
tweetdeck_file.writerow(['user_id', 'tweets'])
for user in data.iterkeys():
    tweetdeck_file.writerow([user, unicode(data.get(user, 'NA')).encode('utf8')])