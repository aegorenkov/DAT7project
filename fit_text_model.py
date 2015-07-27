# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 15:24:49 2015

@author: Alexander
"""

from os import chdir
import pandas as pd
from re import sub
import numpy as np

directory = r'C:\Users\Alexander\Documents\Programming\DAT7\DAT7project'
chdir(directory)

random_user = pd.read_csv(r'data/random_user.csv', nrows=999)
retweeter = pd.read_csv(r'data/retweeter_list.csv')

random_user['user_type'] = 0
retweeter['user_type'] = 1
#Remove any potential id collisions
random_user.rename(columns = {'id':'user_id'}, inplace=True)
random_user = random_user[~random_user["user_id"].isin(retweeter["user_id"])]

random_user = random_user[['user_id', 'user_type']]
retweeter = retweeter[['user_id', 'user_type']]
data = pd.concat([random_user, retweeter], ignore_index=True)

tweetdeck = pd.read_csv(r'data/tweetdeck.csv', nrows=914)
#tweetdeck2 = pd.read_csv(r'data/tweetdeck.csv', skiprows=945, nrows=700)
#tweetdeck =  pd.concat([tweetdeck, tweetdeck2], ignore_index=True)
tweetdeck.tail()
def remove_personal_victories(text):
    return sub('#?[Pp]ersonal[Vv]ictory', '', text)
    
tweetdeck.tweets = tweetdeck.tweets.apply(remove_personal_victories)

data = pd.merge(data, tweetdeck, how='inner')

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(data.tweets, data.user_type, random_state=95)
X_train.shape
X_test.shape

from sklearn.feature_extraction.text import CountVectorizer
vect = CountVectorizer(stop_words='english', min_df=15, ngram_range=(1, 2), binary=True)
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
vect.fit(data.tweets)
all_features = vect.get_feature_names()

# create document-term matrix of ham, then convert to a regular array
ham_dtm = vect.transform(random.tweets)
ham_arr = ham_dtm.toarray()

# create document-term matrix of spam, then convert to a regular array
spam_dtm = vect.transform(retweeter.tweets)
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