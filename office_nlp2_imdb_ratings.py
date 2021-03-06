# -*- coding: utf-8 -*-
"""

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/132NMG5OJmDxFvmyuNR2xtYqIA9DxdZUv

# IMDB MOVIE REVIEW PREDICTION
"""

import numpy as np
import pandas as pd
import re
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
import nltk
nltk.download('stopwords')
import matplotlib.pyplot
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

from bs4 import BeautifulSoup

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv('drive/My Drive/Colab Notebooks/imdb_master.csv', encoding='latin-1')
df_imdb = pd.DataFrame(df,columns=['review','label'])
#unsup is not required for reviews
df_imdb = df_imdb[df_imdb['label'] != 'unsup']

# convert 'neg' and 'pos' into numerical vals
le = LabelEncoder()
df_imdb['label'] = le.fit_transform(df_imdb['label'])
df_imdb.head()

df_lbMaster = pd.read_csv('drive/My Drive/Colab Notebooks/labeledTrainData.tsv',delimiter = '\t')
df_lbMaster.head()

df_lbMaster = df_lbMaster[['review','sentiment']]
df_lbMaster = df_lbMaster.rename(columns = {'sentiment':'label'})
df_lbMaster.head()

df_new_data = pd.concat([df_lbMaster,df_imdb],ignore_index=True) # since both datasets have indexes staring from 0 so after concat it will repeat the index value, hence ignore index
df_new_data.head()

df_new_data.head()
df_new_data['review'][0]

def review_to_words(raw_review):
  corpus = []
  #1. remove html
  review_text = BeautifulSoup(raw_review).get_text()
  #2.
  letters_only = re.sub("[^a-zA-Z]", " ",review_text) # remove all punctuations and numbers and replace with a space
  #3. convert to lower case and split
  words = letters_only.lower().split()
  #4 In python searching a set is much faster than searching in list
  stops = set(stopwords.words('english'))
  #5. Remove stopwords
  meaningful_words = [w for w in words if not w in stops]
  #6
  return(' '.join(meaningful_words))

# Commented out IPython magic to ensure Python compatibility.
# %%time
# #Get number of reviews
# num_reviews = df_new_data['review'].size
# # initialize an empty array 
# clean_train_reviews = []
# # loop over each review 
# print("Cleaning and parsing.....\n")
# for i in range(0,num_reviews):
#   if((i+1)%10000 == 0):
#     print("Review %d of %d \n"%(i+1,num_reviews))
#   clean_train_reviews.append(review_to_words(df_new_data['review'][i]))

cv = CountVectorizer(max_features = 6000)
X = cv.fit_transform(clean_train_reviews)
y = df_new_data['label'].values

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.2)

X.shape

# Commented out IPython magic to ensure Python compatibility.
# %%time
# print("Training the model using count vectorization model...\n")
# classifier_cv = RandomForestClassifier(n_estimators = 10)
# classifier_cv.fit(X_train,y_train)
# y_pred = classifier_cv.predict(X_test)
# print("Accuracy score is: ",accuracy_score(y_pred,y_test))

x_data = clean_train_reviews
X_train,X_test,y_train,y_test = train_test_split(x_data,df_new_data['label'].values, test_size = 0.2)

# Word level TF-idf
tfidf_vect = TfidfVectorizer(max_features = 6000)

# we fit the complete data into the tfidf_vect object to get all features
tfidf_vect.fit(x_data)

# based on tfidf_vect object we transform training and testing data
xtrain_tfidf = tfidf_vect.transform(X_train)
xtest_tfidf = tfidf_vect.transform(X_test)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# print("trainig your TFIDF model...\n")
# classifier_tfidf = RandomForestClassifier(n_estimators = 10)
# classifier_tfidf.fit(xtrain_tfidf,y_train)
# y_pred_tfidf = classifier_tfidf.predict(xtest_tfidf)
# print("Accuracy score is: ",accuracy_score(y_pred_tfidf,y_test))

sentence = ['An experience youll gonna remember forever.']
sentence = cv.transform(sentence)

# predict using CountVectorizer

sentence2 = ['John Wick is something special. It takes as much time setting up elaborate action sequences as it does the world with which it all takes place in']
sentence2 = cv.transform(sentence2)

print('0 for negative review \n 1 for positive review')

classifier_cv.predict(sentence), classifier_cv.predict(sentence2)



