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

class UserLoader(object):
    """
    Helper class to load timelines data from scraped json files
    user_type must be one of 'random', 'retweeter'        
    """
    def __init__(self, directory, user_type):
        if user_type == 'random':
            self.directory = directory + r'\random_users'
        elif user_type == 'retweeter':
            self.directory = directory + r'\retweeting_users'
        else:
            raise ValueError("user_type must be one of 'random' or 'retweeter'")
                
        self._json = []
        self._users = DataFrame()

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
        user_json = listdir(self.directory)
        def load_file(user):
            """Returns line or flag from json file"""
            line = self.get_json_file(user, self.directory)
            if line=='{"message": "This id is not associated with a user"}':
                return 'removeme'
            return line
        lines = [load_file(timeline) for timeline in user_json]
        lines = [line for line in lines if line != 'removeme']
        self._json = self._json_concat(lines)

    @property
    def users(self):
        """Returns pandas dataframe of user statuses"""
        if not self._json:
            self.get_json_data()
        if self._users.empty:
            self._users = read_json(self._json)
        return self._users
