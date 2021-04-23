#Imports the libraries and read the data files
import random
import re
from nltk.stem.snowball import SnowballStemmer
import os
import gensim
from gensim.models import Doc2Vec
from nltk.corpus import stopwords
import nltk
from sklearn.cluster import KMeans
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

from util import *
#nltk.download('stopwords')
#nltk.download('punkt')

path = r'stops.txt'             #Add the path to stopwords_not_to_be_used.txt file
def get_stopwords(path):
  stopwords = nltk.corpus.stopwords.words('spanish')
  not_words = []
  with open(path,'r') as f:
    not_words.append(f.readlines())
  not_words = [word.replace('\n','') for words in not_words for word in words]
  not_words = set(not_words)
  stopwords = set(stopwords)
  customized_stopwords = list(stopwords - not_words)
  return stopwords,customized_stopwords

stop_words,customized_stopwords = get_stopwords(path)

def tokenize(train_texts):
  filtered_tokens = []
  tokens = [word for sent in nltk.sent_tokenize(train_texts) for word in nltk.word_tokenize(sent)]
  for token in tokens:
    if re.search('[a-zA-Z]',token):
        if (('http' not in token) and ('@' not in token) and ('<.*?>' not in token) and token.isalnum() and (not token in stop_words)):
            filtered_tokens.append(token)
  return filtered_tokens

def tokenize_stem(train_texts):
  tokens = tokenize(train_texts)
  stemmer = SnowballStemmer('spanish')
  stemmed_tokens = [stemmer.stem(token) for token in tokens]
  return stemmed_tokens

path = r'TEXTOS/TODOS/'  #Add the path to Articles folder
seed = 137
def load_data(path,seed):
  train_texts = []; filenames = []
  for fname in sorted(os.listdir(path)):
    if fname.endswith('.txt'):
        with open(os.path.join(path,fname),'r') as f:
            train_texts.append(f.read())
        filenames.append(fname)
  #random.seed(seed)
  #random.shuffle(train_texts)
  return train_texts, filenames

train_texts, filenames = load_data(path,seed)
print('FILES:', len(filenames))
LabeledSentence1 = gensim.models.doc2vec.TaggedDocument
all_content = []; j=0;k=0
vocab_tokenized = []; vocab_stemmed = []

for text in train_texts:
    allwords_tokenized = tokenize(text)
    vocab_tokenized.append(allwords_tokenized)
    allwords_stemmed = tokenize_stem(text)
    vocab_stemmed.append(allwords_tokenized)

for text, filename in zip(vocab_tokenized, filenames):
    if len(text)>0:
        all_content.append(LabeledSentence1(text,[j, filename]))  # tagged!
        j+=1
    k+=1

print("Number of emails processed: ", k)
print("Number of non-empty emails vectors: ", j)

#"""**Create a model using Doc2Vec and train it**"""
if False:
    model = pload('modelo2.pk')
    kmeans_model, labels, clusters = model['kmeans']
    pca, datapoint = model['pca'] 
    d2v_model = model['d2v']
                
    print('MODEL reloaded')
else:
    print('TRAINING Doc2Vec model')
    d2v_model = Doc2Vec(all_content, vector_size = 2000, min_count = 5,dm = 0, 
                alpha=0.0025, min_alpha=0.0001)

    d2v_model.train(all_content, total_examples=d2v_model.corpus_count, epochs=50, start_alpha=0.002, end_alpha=-0.016)

    print('Clustering content')
    K_value = 4
    kmeans_model = KMeans(n_clusters = K_value, init='k-means++', n_init = 2000, max_iter = 6000)  
    X = kmeans_model.fit(d2v_model.docvecs.doctag_syn0)
    labels = kmeans_model.labels_.tolist()
    clusters = kmeans_model.fit_predict(d2v_model.docvecs.doctag_syn0)
    print('PCA')

    l = kmeans_model.fit_predict(d2v_model.docvecs.vectors_docs)
    pca = PCA(n_components=2).fit(d2v_model.docvecs.vectors_docs)
    datapoint = pca.transform(d2v_model.docvecs.vectors_docs)

#plt.figure
label1 = ["#FFFF00", "#008000", "#0000FF", "#800080"]
color = [label1[i] for i in labels]
#plt.scatter(datapoint[:, 0], datapoint[:, 1], c=color)

centroids = kmeans_model.cluster_centers_
centroidpoint = pca.transform(centroids)
#plt.scatter(centroidpoint[:, 0], centroidpoint[:, 1], marker='^', s=150, c='#000000')
#plt.savefig('cluster1.png')
#plt.show()

# save it all for future ref:
#import pickle
modelos = {'kmeans': (kmeans_model, labels, clusters),
            'pca': (pca, datapoint), 'd2v': d2v_model, 'all': all_content}
#pickle.dump(modelos, open('modelo2.pk','wb'))
#pickle.dump(all_content, open('all_content.pk','wb'))