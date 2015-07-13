# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 21:43:33 2015

@author: Alexander
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from os import chdir

directory = u'C:\\Users\\Alexander\\Documents\\Programming\\DAT7\\personalvictory_full'
chdir(directory)

random_users = pd.read_csv(r'data/random_user.csv')
victory_users = pd.read_csv(r'data/victory_user.csv')

random_users['user_group'] = 'random_user'
victory_users['user_group'] = 'victory_user'

data = pd.concat([random_users, victory_users], ignore_index=True)
data['created_timestamp'] = pd.to_datetime(data['created_at'])
data['status_timestamp'] = pd.to_datetime(data['status_created_at'])
data.shape
data.describe()

sns.boxplot(vals=data.created_timestamp, groupby=data.user_group)

favorites = sns.boxplot(vals=data.favourites_count, groupby=data.user_group)
favorites.set(yscale="log")

followers = sns.boxplot(vals=data.followers_count, groupby=data.user_group)
followers.set(yscale="log")

friends = sns.boxplot(vals=data.friends_count, groupby=data.user_group)
friends.set(yscale="log")

sns.set_context("poster")
plt.figure(figsize=(20, 16))
test = sns.boxplot(vals=data.statuses_count, groupby=data.user_group)
test.set(yscale="log")
test.set_xlabel("User Group")
test.set_ylabel("Number of Statuses Posted")
test.set_title("Status Count Between #personalvictory and Random Users")
plt.savefig('figures/status_boxplot.png')
#TODO: Do a search using the live tab in twitter

