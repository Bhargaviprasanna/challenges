# -*- coding: utf-8 -*-
"""HackerEarthMothersDayChallenge.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wraL7fGULQC5kfjA1nIyLfaUazAI_W29

## Importing the libraries
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""## Combine both train and test data to form sparse matrix of 'original_text'"""

a = pd.read_csv('train.csv')
train_row_count = len(a.index)
b = pd.read_csv('test.csv')
test_row_count = len(b.index)
merged = pd.concat([a,b], axis=0)
merged.to_csv('Reviews.csv', index=False)
# print(train_row_count, test_row_count)
# 3235+1387

"""## Importing the dataset"""

#Merged test and train set as Reviews.csv
dataset = pd.read_csv('Reviews.csv')
total_count = train_row_count + test_row_count
# print(dataset.head(5)) 
# 0 for Neutral , 1 for Positive, -1 for Negative
dataset = dataset.loc[:, ['original_text','sentiment_class']].values
# dataset[1][0]

"""## Cleaning the texts"""

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []
for i in range(0, 4622):
    review = re.sub('[^a-zA-Z]', ' ', dataset[i][0])
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    review = ' '.join(review)
    corpus.append(review)

"""## Creating the Bag of Words model"""

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 1765)
X = cv.fit_transform(corpus).toarray()
y = dataset[:, -1]
y = y.astype('float')

"""## Splitting the dataset into the Training set and Test set"""

X_train = X[:train_row_count]
X_test = X[train_row_count:]
y_train = y[:train_row_count]
y_train = y_train.astype('int')

"""## Random Forest Classifier"""

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

"""## Predicting the Train set results"""

y_pred = classifier.predict(X_train)
# y_pred

"""## Making the Confusion Matrix"""

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_train, y_pred)
print(cm)
""" for n =100 [[ 764    5    0]
 [   0 1701    0]
 [   2    2  761]]
 # n = 10 [[ 749   20    0]
 [   4 1697    0]
 [   6   51  708]]"""

"""## Score calculation"""

from sklearn.metrics import f1_score
score = 100*f1_score(y_train, y_pred, average='weighted')
score
#97.48139886434113

"""## Predicting the Test set results"""

y_pred = classifier.predict(X_test)

"""## Final Submission file of id, sentiment_class"""

p = pd.read_csv('Reviews.csv')
d = p.iloc[3235:, 0].values
dict = {'id': d, 'sentiment_class': y_pred}
df = pd.DataFrame(dict)
df.to_csv('submission_file.csv', index = False)