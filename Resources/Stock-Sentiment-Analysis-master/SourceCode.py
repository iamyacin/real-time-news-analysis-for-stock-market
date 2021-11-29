# -*- coding: utf-8 -*-
"""
Created on Sun May 24 04:51:18 2020

@author: Yaçin
"""

import pandas as pd

df=pd.read_csv('Data.csv', encoding = "ISO-8859-1")#, engine = 'python')

target = df.iloc[:,1].values

text = df.iloc[:,2:]

for col in text.columns:
    text[col] = text[col].str.lower()

del col

headlines = []
for row in range(0,len(text.index)):
    headlines.append(' '.join(str(x) for x in text.iloc[row,0:25]))

del row

import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Functiion to transform text : 
def txt_transform(txt):
    if isinstance(txt, list) :
        corpus = []
        for sen in txt:
            if isinstance(sen, str): 
                sentence = re.sub('[^a-zA-Z]', ' ', sen)
                sentence = sentence.lower()
                sentence = sentence.split()
                ps = PorterStemmer()
                sentence = [ps.stem(word) for word in sentence if not word in set(stopwords.words('english'))]
                sentence = ' '.join(sentence)
                corpus.append(sentence)
            else :
                print('Value is not String please enter a string value')
        return corpus
    elif isinstance(txt, str) :
        new_txt = re.sub('[^a-zA-Z]', ' ', txt)
        new_txt = new_txt.lower()
        ps = PorterStemmer()
        new_txt = [ps.stem(word) for word in new_txt if not word in set(stopwords.words('english'))]
        new_txt = ' '.join(new_txt)
        return new_txt
    else :
        print('Please enter a string or list of string values')
        
new_headlines = txt_transform(headlines)


# Tokenization :
from nltk import tokenize
tok = tokenize.sent_tokenize(headlines[1])

from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
sid.polarity_scores(df.iloc[1,4])
for sent in tok:
    print(sent)
    print(sid.polarity_scores(sent))
    

from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(ngram_range=(2,2), max_features=250000)
headlines_vector=cv.fit_transform(new_headlines)

vec = headlines_vector.toarray()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(vec, target, test_size = 0.1, random_state = 0)


from sklearn.tree import DecisionTreeClassifier

Classifier = DecisionTreeClassifier()
Classifier.fit(X_train, y_train)
y_pred = Classifier.predict(X_test)

from sklearn.metrics import accuracy_score, confusion_matrix

accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
