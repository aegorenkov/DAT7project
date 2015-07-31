# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 14:09:37 2015

@author: Alexander
"""

from os import chdir
from os import listdir
from pandas import DataFrame, read_json

DIRECTORY = r'C:\Users\Alexander\Documents\Programming\DAT7\DAT7project'
chdir(DIRECTORY)

class UserTimelineLoader(object):
    """Helper class to load timelines data from scraped json files"""
    def __init__(self, directory):
        self.directory = directory + r'\user_timelines'
        self._json = []
        self._timelines = DataFrame()

    @staticmethod
    def get_json_file(filename, directory):
        """Returns single line json data as string from json files"""
        with open(directory + '/' + filename, 'r') as json_file:
            json_data = json_file.read()
            json_file.close()
        return json_data

    @staticmethod
    def _json_concat(list_json):
        """Returns a single string of valid json from a list of json nodes"""
        return '[' + ','.join(list_json) + ']'

    def get_json_data(self):
        """Sets json data as a single string"""
        user_timelines_json = listdir(self.directory)
        def load_file(timeline):
            """Returns line or flag from json file"""
            if timeline.split('_')[1].startswith('fail'):
                return 'removeme'
            if timeline.split('_')[1].startswith('N'):
                return 'removeme'
            line = self.get_json_file(timeline, self.directory)
            return line
        lines = [load_file(timeline) for timeline in user_timelines_json]
        lines = [line for line in lines if line != 'removeme']
        self._json = self._json_concat(lines)

    @property
    def timelines(self):
        """Returns pandas dataframe of user statuses"""
        if not self._json:
            self.get_json_data()
        if self._timelines.empty:
            self._timelines = read_json(self._json)
        return self._timelines
#==============================================================================
# def get_json_data(filename, directory):
#     with open(directory + '/' + filename, 'r') as f:
#         json_data = json.loads(f.read())
#     f.close()
#     return json_data
#     
# data = dict()
# user_timelines_json = listdir(directory + r'/user_timelines')
# for timeline in user_timelines_json:
#     if timeline.split('_')[1].startswith('fail'):
#         continue
#     if timeline.split('_')[1].startswith('N'):
#         continue
#     line = get_json_data(timeline, directory + r'/user_timelines')
#     data_entry = data.get(line['user']['id'], False)
#     if data_entry:
#         data_entry.append(line['text'])
#     else:
#         data[line['user']['id']] = [line['text']]
#     
# for key in data.iterkeys():
#     data[key] = ''.join(data[key])
#     
# tweetdeck_file = csv.writer(open(directory + '\\data\\tweetdeck.csv', 'wb'))
# tweetdeck_file.writerow(['user_id', 'tweets'])
# for user in data.iterkeys():
#     tweetdeck_file.writerow([user, unicode(data.get(user, 'NA')).encode('utf8')])
#==============================================================================
