# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 15:24:49 2015

@author: Alexander
"""

from os import chdir, listdir
import pandas as pd
from re import sub
import numpy as np
from loaders.user_timelines import UserTimelineLoader

DIRECTORY = r'C:\Users\Alexander\Documents\Programming\DAT7\DAT7project'
chdir(DIRECTORY)

#Load in data that determines user categories
random_user = pd.read_csv(r'data/random_user.csv', nrows=999)
random_user.rename(columns = {'id':'user_id'}, inplace=True)
random_user = random_user[['user_id', 'user_type']]
random_user['user_type'] = 0

retweeter = pd.read_csv(r'data/retweeter_list.csv')
retweeter = retweeter[['user_id', 'user_type']]
retweeter['user_type'] = 1

#Remove any potential id collisions
random_user = random_user[~random_user["user_id"].isin(retweeter["user_id"])]

data = pd.concat([random_user, retweeter], ignore_index=True)

#Load in tweet data
#TODO: Add a way to remove personal victories tweets
def remove_personal_victories(text):
    return sub('#?[Pp]ersonal[Vv]ictory', '', text)

def get_user(user_line):
    return user_line.get('id', 'NA')

def df_in_chunks(df, chunksize=25000):
    chunk = 0
    while not df.empty:
        yield (df[:chunksize], chunk)
        df = df[chunksize:]
        chunk +=1
    
#Check for tweet data in data folder, create it if it's not there
if 'tweetdeck.csv' not in listdir(DIRECTORY + r'\data'):
    timeline_loader = UserTimelineLoader(DIRECTORY)
    tweetdeck = timeline_loader.timelines
    dchunks = df_in_chunks(tweetdeck)
    for dchunk in dchunks:
        dchunk[0].to_csv(DIRECTORY + r'\data' + r'\tweetdeck'+str(dchunk[1])+'.csv', encoding = 'utf8', engine='python')
    
#Read in tweet data and reshape it to user-level data by appending together tweets
filenames = [f for f in listdir(DIRECTORY + r'\data') if f.startswith('tweetdeck')]
#Read the csv files in chunks
tweetdeck = pd.concat(
    [pd.read_csv(DIRECTORY + '\data' + '\\' + name, encoding='utf8', engine='python') for name in filenames], 
     ignore_index=True)
tweetdeck['user_id'] = tweetdeck.user.apply(get_user)
tweetdeck = tweetdeck.groupby('user_id')['text'].sum() #This actually appends text together
tweetdeck = pd.DataFrame(tweetdeck)
tweetdeck['user_id'] = tweetdeck.index    
tweetdeck.text = tweetdeck.text.apply(remove_personal_victories)

#Merge user categories and tweet data together
data = pd.merge(data, tweetdeck, how='inner')

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(data.text, data.user_type, random_state=95)
X_train.shape
X_test.shape

from sklearn.feature_extraction.text import CountVectorizer
vect = CountVectorizer(stop_words='english', min_df=15, ngram_range=(1, 2), binary=False, max_features = 50)
train_dtm = vect.fit_transform(X_train)
train_dtm

# transform testing data into a document-term matrix
test_dtm = vect.transform(X_test)
test_dtm

# train a Naive Bayes model using train_dtm
from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB(alpha=0.005)
nb.fit(train_dtm, y_train)

# make predictions on test data using test_dtm
y_pred_class = nb.predict(test_dtm)

# compare predictions to true labels
from sklearn import metrics
print metrics.accuracy_score(y_test, y_pred_class)
print metrics.confusion_matrix(y_test, y_pred_class)

print metrics.accuracy_score(y_test, y_pred_class*0)


# predict (poorly calibrated) probabilities and calculate AUC
y_pred_prob = nb.predict_proba(test_dtm)[:, 1]
y_pred_prob
print metrics.roc_auc_score(y_test, y_pred_prob)


X_test[y_test < y_pred_class]
X_test[y_test > y_pred_class]


# create separate DataFrames for ham and spam
random = data[data.user_type == 0]
retweeter = data[data.user_type == 1]

# learn the vocabulary of ALL messages and save it
vect.fit(data.text)
all_features = vect.get_feature_names()

# create document-term matrix of ham, then convert to a regular array
ham_dtm = vect.transform(random.text)
ham_arr = ham_dtm.toarray()

# create document-term matrix of spam, then convert to a regular array
spam_dtm = vect.transform(retweeter.text)
spam_arr = spam_dtm.toarray()

# count how many times EACH token appears across ALL messages in ham_arr
ham_counts = np.sum(ham_arr, axis=0)

# count how many times EACH token appears across ALL messages in spam_arr
spam_counts = np.sum(spam_arr, axis=0)

# create a DataFrame of tokens with their separate ham and spam counts
all_token_counts = pd.DataFrame({'token':all_features, 'ham':ham_counts, 'spam':spam_counts})

# add one to ham counts and spam counts so that ratio calculations (below) make more sense
all_token_counts['ham'] = all_token_counts.ham + 1
all_token_counts['spam'] = all_token_counts.spam + 1

# calculate ratio of spam-to-ham for each token
all_token_counts['spam_ratio'] = all_token_counts.spam / all_token_counts.ham
all_token_counts.sort('spam_ratio')