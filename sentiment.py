import numpy as np  # https://numpy.org/doc/
from afinn import Afinn  # https://pypi.org/project/afinn/
import matplotlib.pyplot as plt  # https://matplotlib.org/stable/index.html
import pandas as pd  # https://pandas.pydata.org/docs/
from utils import save_df_as_txt


def score(texts, labels, k, doc_name):
    """
    calculates sentiment value for each document usind the Afinn package
    plots and returns different measures for analysis
    """
    scores = [[] for _ in range(k)]
    scores2 = []
    names = []
    afinn = Afinn()
    # print(labels)
    labels2 = []
    for i in range(k):
        for index, text in enumerate(texts):
            if labels[index] == i:
                score = afinn.score(text)
                scores2.append(score)
                names.append(doc_name[index])
                # print(doc_name[index],score)
                scores[i].append(score)
                labels2.append(i)
            # print(afinn.score(text))
    count_cluster = []
    for i in range(k):
        count_cluster.append(np.count_nonzero(labels == i))
    df2 = pd.DataFrame()
    df2['name'] = names
    df2['scores'] = scores2
    df2['label'] = labels2
    print(df2)
    save_df_as_txt(df2, 'doc_name_sentiment_label_' + str(k) + '.txt')
    x = list(range(0, k))
    df1 = pd.DataFrame()
    df1['cluster'] = x
    df1['min'] = [np.min(scores[i]) for i in range(k)]
    df1['max'] = [np.max(scores[i]) for i in range(k)]
    df1['median'] = [np.median(scores[i]) for i in range(k)]
    df1['mean'] = [round(np.mean(scores[i]), 1) for i in range(k)]
    print(df1)
    save_df_as_txt(df1, 'sentiment_of_cluster_' + str(k) + '.txt')
    for i in range(k):
        for j in scores[i]:
            plt.scatter(i, j)
        plt.scatter(i, np.mean(scores[i]), c='blue', marker='X', s=75)
    plt.title('sentiment scores of documents with ' + str(k) + ' clusters')
    plt.xticks(x, ['cluster' + str(i) for i in x])
    plt.ylabel('sentiment score')
    plt.show()
    print('Top 5 documents with highest sentiment')
    for i in np.argsort(scores2)[::-1][:5]:
        print(names[i], scores2[i])
    print('Top 5 documents with lowest sentiment')
    for i in np.argsort(scores2)[:5]:
        print(names[i], scores2[i])
