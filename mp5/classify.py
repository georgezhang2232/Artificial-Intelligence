# classify.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018
# Extended by Daniel Gonzales (dsgonza2@illinois.edu) on 3/11/2020

import numpy as np
"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.

train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
            This can be thought of as a list of 7500 vectors that are each
            3072 dimensional.  We have 3072 dimensions because there are
            each image is 32x32 and we have 3 color channels.
            So 32*32*3 = 3072. RGB values have been scaled to range 0-1.

train_labels - List of labels corresponding with images in train_set
example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
         and X1 is a picture of a dog and X2 is a picture of an airplane.
         Then train_labels := [1,0] because X1 contains a picture of an animal
         and X2 contains no animals in the picture.

dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
          It is the same format as train_set
"""

def trainPerceptron(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained weight and bias parameters 
    length = len(train_set[0])
    W = np.zeros(length)
    b = 0
    for k in range(max_iter):
        for i in range(len(train_set)):
            sign = np.sign(np.dot(train_set[i], W) + b)
            if sign == 1:
                if train_labels[i] != 1:
                    W -= train_set[i] * learning_rate
                    b -= learning_rate
            else:
                if train_labels[i] != 0:
                    W += train_set[i] * learning_rate
                    b += learning_rate
    return W, b

def classifyPerceptron(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train perceptron model and return predicted labels of development set
    W, b = trainPerceptron(train_set, train_labels, learning_rate, max_iter)
    dev_label = []
    for data in dev_set:
        sign = np.sign(np.dot(W, data) + b)
        if sign == 1:
            dev_label.append(1)
        else:
            dev_label.append(0)
    return dev_label

def sigmoid(x):
    # TODO: Write your code here
    # return output of sigmoid function given input x
    return 1 / (1 + np.exp(-x))

def trainLR(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained weight and bias parameters 
    length = len(train_set[0])
    W = np.zeros(length)
    b = 0
    len2 = len(train_labels)
    for i in range(max_iter):
        res = np.dot(train_set, W)+b
        sig = sigmoid(res)
        ly = (sig - train_labels) / (sig - np.multiply(sig, sig))
        gradient = np.exp(-res)/(1 + np.exp(-res))**2
        base = np.multiply(ly, gradient)
        W -= learning_rate * np.dot(base, train_set) / len2
        b -= learning_rate * sum(base) / len2
    return W, b

def classifyLR(train_set, train_labels, dev_set, learning_rate, max_iter):
    W, b = trainLR(train_set, train_labels, learning_rate, max_iter)
    dev_label = []
    for data in dev_set:
        sign = round(sigmoid(np.dot(W,data) + b))
        if sign == 1:
            dev_label.append(1)
        else:
            dev_label.append(0)
    return dev_label
    # TODO: Write your code here
    # Train LR model and return predicted labels of development set
    return []

def classifyEC(train_set, train_labels, dev_set, k):
    # Write your code here if you would like to attempt the extra credit
    return []
