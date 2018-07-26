#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import urllib.request, urllib.error, urllib.parse
from collections import Counter

import math
from bs4 import BeautifulSoup


def vector_subtract(v, w):
    """subtracts two vectors componentwise"""
    return [v_i - w_i for v_i, w_i in zip(v, w)]


def dot(v, w):
    """v_1 * w_1 + ... + v_n * w_n"""
    return sum(v_i * w_i for v_i, w_i in zip(v, w))


def sum_of_squares(v):
    """v_1 * v_1 + ... + v_n * v_n"""
    return dot(v, v)


def squared_distance(v, w):
    return sum_of_squares(vector_subtract(v, w))


def distance(v, w):
    return math.sqrt(squared_distance(v, w))


def majority_vote(labels):
    """assumes that labels are ordered from nearest to farthest"""
    vote_counts = Counter(labels)
    winner, winner_count = vote_counts.most_common(1)[0]
    num_winners = len([count
                       for count in list(vote_counts.values())
                       if count == winner_count])

    if num_winners == 1:
        return winner  # unique winner, so return it
    else:
        return majority_vote(labels[:-1])  # try again without the farthest


def knn_classify(k, labeled_points, new_point):
    """each labeled point should be a pair (point, label)"""

    # order the labeled points from nearest to farthest
    by_distance = sorted(labeled_points,
                         key=lambda point__: distance(point__[0], new_point))

    # find the labels for the k closest
    k_nearest_labels = [label for _, label in by_distance[:k]]

    # and let them vote
    return majority_vote(k_nearest_labels)


if __name__ == '__main__':

    html = urllib.request.urlopen("http://tool.chinaz.com/Tools/web").read()
    soup = BeautifulSoup(html, "lxml")
    labeled_colors = []
    for color in soup.select("div.color"):
        red = int(color.select_one(".red").text)
        green = int(color.select_one(".green").text)
        blue = int(color.select_one(".blue").text)
        rgb = color.select(".html b")[1].text.strip()
        labeled_colors.append(([red, green, blue], rgb))
    with open("labeled_colors.pkl", 'wb') as f:
        pickle.dump(labeled_colors, f)
    with open("labeled_colors.pkl", 'rb') as f:
        labeled_colors = pickle.load(f)
        print(labeled_colors)
    print(knn_classify(1, labeled_colors, [1, 253, 1]))
