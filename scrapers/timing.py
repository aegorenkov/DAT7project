# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 21:31:35 2015

@author: Alexander
"""

from time import time

class ScrapeTimer(object):
    def __init__(self):
        self.time = time()
        
    def set_next_run(self, rate):
        self.time = self.time + rate
        
    def ready(self):
        return self.time < time()
        