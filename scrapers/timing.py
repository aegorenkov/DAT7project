# -*- coding: utf-8 -*-
"""
This module creates a simple timer to manage requests to various scrapers.
By setting the next allowable time for a scraper to run we can delay scrapers
through an event loop rather than running multiple threads.
"""

from time import time

class ScrapeTimer(object):
    def __init__(self):
        self.time = time()
        
    def set_next_run(self, rate):
        self.time = self.time + rate
        
    def ready(self):
        return self.time < time()
        