#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud

back_coloring = imread("nlp/mask.jpg")
wordcloud = WordCloud(font_path=u'nlp/文泉驿微米黑.ttf', background_color="white", mask=back_coloring)


def show_wordcloud(data):
    plt.axis("off")
    wc_img = wordcloud.fit_words(data)
    plt.imshow(wc_img)
    plt.axis("on")


def search_path(o, to):
    path = ""
    for k, v in o.items():
        if isinstance(v, dict):
            sub = search_path(v, to)
            if sub:
                path = k + "." + sub
        else:
            if to == v:
                path = k
    return path


def leaf_path(o):
    print o
    for k, v in o.items():
        if isinstance(v, dict):
            subs = leaf_path(v)
            for sub_k, sub_v in subs:
                yield k + "." + sub_k, sub_v
        else:
            yield k, v


with codecs.open(u"nlp/name_start.txt", 'r', 'utf-8') as fp:
    name_start = fp.readlines()
name_start = [start.strip() for start in name_start]


def name_start_set():
    return name_start


def start_with(p, items):
    for item in items:
        if p.startswith(item):
            return True
    return False


def end_with(p, items):
    for item in items:
        if p.endswith(item):
            return True
    return False


if __name__ == '__main__':
    pass
