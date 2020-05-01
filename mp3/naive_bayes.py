# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
# Modified by Jaewook Yeom 02/02/2020

"""
This is the main entry point for Part 1 of MP3. You should only modify code
within this file for Part 1 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as numpy
import math
from collections import Counter


def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter you provided with --laplace (1.0 by default)

    pos_prior - positive prior probability (between 0 and 1)
    """
    # TODO: Write your code here
    cnt_p = Counter()
    cnt_n = Counter()
    length = len(train_labels)
    for i in range(length):
        if train_labels[i] == 1:
            cnt_p.update(train_set[i])
        else:
            cnt_n.update(train_set[i])
    sum_p = sum(cnt_p.values())
    sum_n = sum(cnt_n.values())
    distinct_p = len(list(cnt_p))
    distinct_n = len(list(cnt_n))
    res = []

    for review in dev_set:
        post_p = math.log(pos_prior)
        post_n = math.log(1 - pos_prior)
        for word in review:
            if cnt_p[word] == 0:
                distinct_p += 1
                distinct_n += 1
            p_like = ((cnt_p[word] + smoothing_parameter) / (smoothing_parameter * distinct_p + sum_p))
            n_like = ((cnt_n[word] + smoothing_parameter) / (smoothing_parameter * distinct_n + sum_n))
            post_p += math.log(p_like)
            post_n += math.log(n_like)
        if post_p > post_n:
            res.append(1)
        else:
            res.append(0)
    # return predicted labels of development set (make sure it's a list, not a numpy array or similar)
    return res