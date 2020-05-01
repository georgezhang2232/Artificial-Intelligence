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
This is the main entry point for Part 2 of this MP. You should only modify code
within this file for Part 2 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


import numpy as numpy
import math
from collections import Counter





def naiveBayesMixture(train_set, train_labels, dev_set, bigram_lambda,unigram_smoothing_parameter, bigram_smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    bigram_lambda - float between 0 and 1

    unigram_smoothing_parameter - Laplace smoothing parameter for unigram model (between 0 and 1)

    bigram_smoothing_parameter - Laplace smoothing parameter for bigram model (between 0 and 1)

    pos_prior - positive prior probability (between 0 and 1)
    """
 


    # TODO: Write your code here
    cnt_p = Counter()
    cnt_n = Counter()
    bi_p = Counter()
    bi_n = Counter()
    length = len(train_labels)
    for i in range(length):
        if train_labels[i] == 1:
            cnt_p.update(train_set[i])

            temp = []
            for j in range(len(train_set[i]) - 1):
                temp.append(train_set[i][j] + " " + train_set[i][j+1])
            bi_p.update(temp)            
            
        else:
            cnt_n.update(train_set[i])

            temp = []
            for j in range(len(train_set[i]) - 1):
                temp.append(train_set[i][j] + " " + train_set[i][j+1])
            bi_n.update(temp)    

    sum_p = sum(cnt_p.values())
    sum_n = sum(cnt_n.values())
    distinct_p = len(list(cnt_p))
    distinct_n = len(list(cnt_n))

    sum_p_bi = sum(bi_p.values())
    sum_n_bi = sum(bi_n.values())
    distinct_p_bi = len(list(bi_p))
    distinct_n_bi = len(list(bi_n))

    res = []

    for review in dev_set:
        uni_p_post = math.log(pos_prior)
        bi_p_post = math.log(pos_prior)
        uni_n_post = math.log(1 - pos_prior)
        bi_n_post = math.log(1 - pos_prior)
        for word in review:
            if cnt_p[word] == 0:
                distinct_p += 1
                distinct_n += 1
            p_like = ((cnt_p[word] + unigram_smoothing_parameter) / (unigram_smoothing_parameter * distinct_p + sum_p))
            n_like = ((cnt_n[word] + unigram_smoothing_parameter) / (unigram_smoothing_parameter * distinct_n + sum_n))
            uni_p_post += math.log(p_like)
            uni_n_post += math.log(n_like)
        uni_p_post = uni_p_post * (1 - bigram_lambda)
        uni_n_post = uni_n_post * (1 - bigram_lambda)

        for k in range(len(review) - 1):
            bi_word = review[k] + " " + review[k+1]
            if cnt_p[bi_word] == 0:
                distinct_p_bi += 1
                distinct_n_bi += 1
            p_like_bi = ((bi_p[bi_word] + bigram_smoothing_parameter) / (bigram_smoothing_parameter * distinct_p_bi + sum_p_bi))
            n_like_bi = ((bi_n[bi_word] + bigram_smoothing_parameter) / (bigram_smoothing_parameter * distinct_n_bi + sum_n_bi))
            bi_p_post += math.log(p_like_bi)
            bi_n_post += math.log(n_like_bi)
        bi_p_post = bi_p_post * bigram_lambda
        bi_n_post = bi_n_post * bigram_lambda
        if (uni_p_post + bi_p_post) > (uni_n_post + bi_n_post):
            res.append(1)
        else:
            res.append(0)
    # return predicted labels of development set (make sure it's a list, not a numpy array or similar)
    return res