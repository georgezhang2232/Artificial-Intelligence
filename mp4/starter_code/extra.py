from collections import defaultdict, Counter
import math
import numpy as np
def extra(train,test):
    '''
    TODO: implement improved viterbi algorithm for extra credits.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
            test data (list of sentences, no tags on the words)
            E.g  [[word1,word2,...][word1,word2,...]]
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''
    res = []
    tags = []
    tag_count = {}
    initial = Counter()
    trans = {}
    emission = {}
    hap = {}
    tags = []
    # generate tagset with all distinct tags 
    # initialize transition/emission
    for sentence in train:
        for words in sentence:
            word, tag = words
            initial[tag] = 0
            trans[tag] = {}
            emission[tag] = {}
            tag_count[tag] = 0
            if tag not in tags:
                tags.append(tag)            
    tag_len = len(tags)
    for tag in tags:
        hap[tag] = 0
        for i in trans:
            if tag not in trans[i]:
                trans[i][tag] = 0

    # got initial/transition/emission for all tags and 
    for sentence in train:
        for index, words in enumerate(sentence):
            word, tag = words
            # first word in sentence
            if index == 0:
                initial.update({tag})
            # for each word from 2nd
            if index <= len(sentence) - 2:
                next_tag = sentence[index + 1][1]
                trans[tag][next_tag] += 1
            if word not in emission[tag]:
                emission[tag][word] = 1
            else:
                emission[tag][word] += 1
    ha_count = 0
    for tag in emission:
        for words in emission[tag]:
            if emission[tag][words] == 1:
                hap[tag] += 1
                ha_count += 1
    # soomthing initial, emission, trans and unseen using laplace = 0.00001
    for tag in tags:
        ini_len = len(list(initial))
        initial[tag] = np.log(initial[tag] / ini_len)   
        hap[tag] = np.log(hap[tag]/ha_count)
        # according to eqution log((c+k)/(N+k*X))
        for word in emission[tag]:
            emission[tag][word] = np.log((0.00001 + emission[tag][word]) / (tag_count[tag] + 0.00001 * len(emission[tag])))
        # according to eqution log((c+k)/(N+k*X))
        for next_tag in trans[tag]:
            trans[tag][next_tag] = np.log((0.00001 + trans[tag][next_tag]) / (tag_count[tag] + 0.00001 * tag_len))
 
    for sentence in test:
        temp2 = []
        for index, word in enumerate(sentence):
            temp = []
            # first word in the sentence
            if index == 0:
                for tag in tags:
                    # we saw the word with this tag before or didnt see word with this tag before
                    prob = (initial[tag] + emission[tag][word]) if word in emission[tag] else (initial[tag] + hap[tag])
                    start = [(word, tag)]
                    temp.append((prob, tag, start))
            # else word else in the sentence starting at 2nd
            else:
                for tag in tags:
                    # data for 1st words
                    begin = temp2[0]
                    positon = begin[2]
                    curr = begin[0] + trans[begin[1]][tag]
                    # find out the max probability path
                    for temp3 in temp2:
                        temp_pos = temp3[2]
                        temp_prob = temp3[0] + trans[temp3[1]][tag]
                        if temp_prob > curr:
                            positon = temp_pos
                            curr = temp_prob
                        prob = (curr + emission[tag][word]) if word in emission[tag] else (curr + hap[tag])
                    path = positon.copy()
                    path.append((word, tag))
                    temp.append((prob, tag, path))
            temp2 = temp
            
        finished_sentence = []
        # keep add path for each sentence on the back
        if len(temp2) == 0:
            continue
        else:
            temp2.sort()
            prediction = temp2[-1]
            path = prediction[2]
            finished_sentence.extend(path)
            res.append(finished_sentence)
    return res