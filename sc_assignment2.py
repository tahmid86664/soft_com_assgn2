# -*- coding: utf-8 -*-
"""SC_Assignment2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rBEkagCExlLw7tkRBFRaypuLiz0_R1En

# Importing
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import tensorflow as tf
from tensorflow import keras
import seaborn as sn
from sklearn.model_selection import train_test_split

"""# Mounting"""

from google.colab import drive
drive.mount('/content/drive')

"""# Read dataset"""

url = '/content/drive/My Drive/Colab Notebooks/datasets/text_dataset.csv'

df = pd.read_csv(url)
df.head()

texts = df['Text']
sentiments = df['Sentiment']
print(texts.head())
print(sentiments.head())

sentiments = np.array(sentiments)
sentiments[sentiments < 0] = 0

"""# Pre-processing"""

import nltk
from nltk import corpus

nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
 
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

word_tokens = []

for i in texts:
  word_tokens.append(word_tokenize(i))

# stopwords filtering
stopwords_filtered_texts = []
for t in word_tokens:
    filtered_sentence = []
    for w in t:
      if w not in stop_words:
        filtered_sentence.append(w)
    stopwords_filtered_texts.append(filtered_sentence)

print(word_tokens[2])
print(stopwords_filtered_texts[2])

# stemming
stemmed_texts = []
for t in stopwords_filtered_texts:
  filtered_sent = []
  for w in t:
    filtered_sent.append(ps.stem(w))
  stemmed_texts.append(filtered_sent)

print(stemmed_texts[2])

"""# BoW (Neural Network)"""

import heapq

word_count = {}
for t in stemmed_texts:
  for w in t:
    if w not in word_count.keys():
      word_count[w] = 1
    else:
      word_count[w] += 1
len(word_count)

freq_words = heapq.nlargest(100, word_count, key=word_count.get)  # first parameter holo amra koto word chai
freq_words[:4]

BoW = []
for t in stemmed_texts:
    vector = []
    for w in freq_words:
        if w in t:
            vector.append(1)
        else:
            vector.append(0)
    BoW.append(vector)
BoW = np.asarray(BoW)
print(BoW[:2])

x_train, x_test, y_train, y_test = train_test_split(BoW, sentiments, test_size=0.2, random_state=39)
print(x_train.shape)
print(x_test.shape)
print(y_train.shape)

nn = keras.Sequential([
    keras.layers.Flatten(input_shape=(100, )),
    keras.layers.Dense(500, activation='relu'),
    keras.layers.Dense(100, activation='relu'),
    keras.layers.Dense(100, activation='relu'),
    keras.layers.Dense(2, activation='softmax')
])

adam = keras.optimizers.Adam(learning_rate=0.01)
nn.compile(
    optimizer=adam,
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

nn_history = nn.fit(x_train, y_train, epochs=10, batch_size=39)

plt.plot(nn_history.history['loss'])
plt.title('Loss VS Epoch')
plt.ylabel('Sparse Categorical Crossentropy Value')
plt.xlabel('No. Epoch')
plt.show()

nn.evaluate(x_test, y_test)

from sklearn import metrics
y_predict = nn.predict(x_test)
y_predict_labels = [np.argmax(i) for i in y_predict]
y_predict_labels[:5]

print(metrics.classification_report(y_test, y_predict_labels))
print ('Accuracy: ', metrics.accuracy_score(y_test, y_predict_labels))
print ('Precision: ', metrics.precision_score(y_test, y_predict_labels, average='macro'))
print ('Recall: ', metrics.recall_score(y_test, y_predict_labels, average='macro'))
print ('F1-score: ', metrics.f1_score(y_test, y_predict_labels, average='macro'))

"""# TF-IDF (Neural Network)"""

from sklearn.feature_extraction.text import TfidfVectorizer

# tfidf = TfidfVectorizer(stemmed_texts[])

"""# One-Hot Embedding (CNN)"""

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder