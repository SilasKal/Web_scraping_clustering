import nltk  # https://www.nltk.org/
import os  # https://docs.python.org/3/library/os.html
import sklearn  # https://docs.python.org/3/library/os.html
from sklearn.feature_extraction.text import TfidfVectorizer  # https://scikit-learn.org/stable/
from sklearn.feature_extraction.text import CountVectorizer  # https://scikit-learn.org/stable/
import pandas as pd  # https://pandas.pydata.org/docs/
from sklearn.cluster import KMeans  # https://scikit-learn.org/stable/
import matplotlib.pyplot as plt  # https://matplotlib.org/stable/index.html
import numpy as np  # https://numpy.org/doc/
from sklearn.metrics import silhouette_score  # https://scikit-learn.org/stable/
from sklearn.metrics import calinski_harabasz_score  # https://scikit-learn.org/stable/
from sklearn.metrics import davies_bouldin_score  # https://scikit-learn.org/stable/


def stemmer_remove_stopw(text):
    """
    tokenizes, stems and removes stopwords from given text
    """
    porter_stem = nltk.PorterStemmer()
    tokens = nltk.word_tokenize(text, language='english')
    stop_words = nltk.corpus.stopwords.words('english')
    tokens = [token for token in tokens if
              any(charac.isalnum() for charac in token) and token != '' and token not in stop_words]
    tokens = [porter_stem.stem(token) for token in tokens]
    return tokens


def remove_stopwords(text):
    """
    tokenizes and removes stop words from given text
    """
    tokens = nltk.word_tokenize(text, language='english')
    stop_words = nltk.corpus.stopwords.words('english')
    tokens = [token for token in tokens if
              any(charac.isalnum() for charac in token) and token != '' and token not in stop_words]
    return tokens


def stemmer(text):
    """
    tokenizes, stems given text
    """
    porter_stem = nltk.PorterStemmer()
    tokens = nltk.word_tokenize(text, language='english')
    tokens = [porter_stem.stem(token) for token in tokens]
    return tokens


def read_txt_and_vectorize(input_path, stem=True, remove_stopw=True):
    """
        reads files in given input path and converts text into count matrix
        :param stem: decides whether texts are stemmed or not
        :param input_path: input path of files
        :param remove_stopw: remove stopwords when vectorizing
    """
    path = input_path
    texts = []
    doc_name = {}
    for counter, filename in enumerate(os.listdir(path)):
        with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:  # open in readonly mode
            text = f.read()
            texts.append(text)
            doc_name[counter] = filename
            # print(text)
        f.close()
    if stem and remove_stopw:
        vec = CountVectorizer(tokenizer=stemmer_remove_stopw)
    elif not stem and remove_stopw:
        vec = CountVectorizer(tokenizer=remove_stopwords)
    elif not stem and not remove_stopw:
        vec = CountVectorizer(tokenizer=nltk.word_tokenize)
    elif stem and not remove_stopw:
        vec = CountVectorizer(tokenizer=stemmer)

    matrix = vec.fit_transform(texts)
    return matrix, vec, texts, doc_name


def read_txt_and_tfidf(input_path, stem=True, remove_stopw=True):
    """
    reads files in given input path and converts text into tfidf matrix
    :param stem: decides whether texts are stemmed or not
    :param remove_stopw: remove stopwords or not
    :param input_path: input path of files
    """
    path = input_path
    texts = []
    doc_name = {}
    for counter, filename in enumerate(os.listdir(path)):
        with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:  # open in readonly mode
            text = f.read()
            texts.append(text)
            doc_name[counter] = filename
            # print(text)
        f.close()
    if stem and remove_stopw:
        vec = TfidfVectorizer(norm='l2', tokenizer=stemmer_remove_stopw)
    elif not stem and remove_stopw:
        vec = TfidfVectorizer(norm='l2', tokenizer=remove_stopwords)
    elif not stem and not remove_stopw:
        vec = TfidfVectorizer(norm='l2', tokenizer=nltk.word_tokenize)
    elif stem and not remove_stopw:
        vec = TfidfVectorizer(norm='l2', tokenizer=stemmer)
    matrix = vec.fit_transform(texts)
    return matrix, vec, texts, doc_name


def kmeans_on_text(matrix, vec, k, output_top_terms=False):
    """
    clusters given matrix using Kmeans returns a label for each document
    """
    km = KMeans(n_clusters=k, random_state=0)
    km.fit(matrix)
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    terms = vec.get_feature_names_out()
    if output_top_terms:
        print("Top terms per cluster:")
        f = open('20_most_informative_words_' + str(k) + '.txt', "w", encoding='utf8')
        for i in range(k):
            top_twenty_words = [terms[ind] for ind in order_centroids[i, :20]]
            print("Cluster {}: {}".format(i, ' '.join(top_twenty_words)))
            f.write('\n' + 'Cluster ' + str(i) + ' ' + ' '.join(top_twenty_words))
        f.close()
    return km.labels_


def cluster_assessment(data, num_docs):
    """
    assesses cluster with different measure and plots results
    """
    sse = {}
    s_score = {}
    ch_score = {}
    db_score = {}
    for k in range(1, num_docs):
        kmeans = KMeans(n_clusters=k, random_state=0).fit(data)
        if k >= 2:
            s_score[k] = silhouette_score(data, kmeans.labels_)
            db_score[k] = davies_bouldin_score(data.toarray(), kmeans.labels_)
            ch_score[k] = calinski_harabasz_score(data.toarray(), kmeans.labels_)
        sse[k] = kmeans.inertia_
    for i in [3, 6]:
        print(i, 'clusters silhouette score', s_score[i])
        print(i, 'clusters calinski harabasz score', ch_score[i])
        print(i, 'clusters davies bouldin score', db_score[i])
        print(i, 'clusters SSE', sse[i])
    plt.figure()
    plt.plot(list(sse.keys()), list(sse.values()), label='SSE')
    plt.plot(list(ch_score.keys()), list(ch_score.values()), label='calinski harabasz')
    plt.plot(list(db_score.keys()), list(db_score.values()), label='davies bouldin')
    plt.plot(list(s_score.keys()), list(s_score.values()), label='silhouette')
    plt.legend()
    plt.xlabel("Number of cluster")
    plt.show()
