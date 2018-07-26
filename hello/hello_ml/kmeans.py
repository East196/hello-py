#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import imp

imp.reload(sys)
sys.setdefaultencoding('utf-8')
import codecs

from sklearn.cluster import KMeans
from sklearn.preprocessing import Imputer
import numpy as np
import pandas as pd
import jieba
import jieba.posseg as pseg
import gensim

from .tool import start_with, name_start


def kmeans(model, characters_names):
    all_names = []

    word_vectors = None
    np_names = None
    for name in characters_names:
        if name in model:
            all_names.append(name)
    for name in all_names:
        if word_vectors is None:
            word_vectors = model[name]
        else:
            word_vectors = np.vstack((word_vectors, model[name]))
            np_names = np.array(all_names)

    return np_names, word_vectors


def aggre3(np_names, word_vectors):
    N = 3

    word_vectors = Imputer().fit_transform(word_vectors)
    print(word_vectors)
    label = KMeans(N).fit(word_vectors).labels_

    for c in range(N):
        print(("类别{}：".format(c + 1)))
        for idx, name in enumerate(np_names[label == c]):
            print(name)
            if idx % 10 == 9:
                print('')
        print('')


def print_aggre3(words, names):
    model = gensim.models.Word2Vec(words, size=20, window=5, min_count=5, workers=4)
    np_names, word_vectors = kmeans(model, names)
    aggre3(np_names, word_vectors)


def get_book_lines(book_type, book_name):
    path = "book/%s/%s.txt" % (book_type, book_name)

    with codecs.open(path, 'r', 'utf-8') as fp:
        book_lines = fp.readlines()
    return book_lines



def get_sentences(book_lines):
    sentences = []
    for line in book_lines:
        words = list(jieba.cut(line))
        sentences.append(words)
    return sentences


def get_content(book_type, book_name):
    path = "book/%s/%s.txt" % (book_type, book_name)
    with codecs.open(path, 'r', 'utf-8') as fp:
        content = fp.read()
    return content


def get_segments(content):
    segments = [seg for seg in pseg.cut(content)]
    return segments


def get_df(segments):
    word, flag = list(zip(*segments))
    df = pd.DataFrame({'word': word, "flag": flag})

    stopwords = pd.read_csv("nlp/stop_words.txt")
    df = df[~df.word.isin(stopwords.stopword)]
    return df


def get_names(df):
    nrdf = df[df.flag == "nr"]
    nrdf = nrdf[df.word.apply(lambda word: len(word) > 1 and start_with(word, name_start))]
    nrStat = nrdf.groupby(by=["word"])["word"].agg({"count": np.size}).reset_index().sort_values(by=["count"], ascending=False);
    nr = nrStat[nrStat["count"] > 10]
    print(nr.count())
    return nr['word'].tolist()


if __name__ == '__main__':
    book_type, book_name = "仙侠", "仙葫"
    content = get_content(book_type, book_name)
    segments = get_segments(content)
    sentences = get_sentences(get_book_lines(book_type, book_name))
    df = get_df(segments)
    names = get_names(df)
    print_aggre3(sentences, names)
