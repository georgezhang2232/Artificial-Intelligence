"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import numpy as np
from collections import Counter
def baseline(train, test):
    '''
    TODO: implement the baseline algorithm. This function has time out limitation of 1 minute.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
            test data (list of sentences, no tags on the words)
            E.g  [[word1,word2,...][word1,word2,...]]
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''
    db = {}
    res = []
    max_len = 0
    max_tag = ""
    # build db for each tag-word pair
    for sentence in train:
        for word in sentence:
            tag = word[1]
            db[tag] = {}
    for sentence in train:
        for words in sentence:
            word, tag = words
            if word not in db[tag]:
                db[tag][word] = 1
            else:
                db[tag][word] += 1
    # find the most frequent word
    for tag in db:
        temp_len = len(db[tag])
        if  temp_len >= max_len:
            max_len = temp_len
            max_tag = tag

    for sentence in test:
        temp = []
        for word in sentence:
            maximum = 0
            temp_tag = max_tag
            # for each word, find the maximum appearance of the tag
            # if not seen before, using the most frequent tag in the db
            for tag in db:
                count = db[tag].get(word)
                if count != None:
                    if count > maximum:
                        maximum = count
                        temp_tag = tag
            temp.append((word,temp_tag))
        res.append(temp)            

    return res

def viterbi_p1(train, test):
    '''
    TODO: implement the simple Viterbi algorithm. This function has time out limitation for 3 mins.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words)
            E.g [[word1,word2...]]
    output: list of sentences with tags on the words
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''
    res = []
    tags = []
    tag_count = Counter()
    initial = Counter()
    trans = {}
    emission = {}
    tags = []
    # generate tagset with all distinct tags 
    # initialize transition/emission
    for sentence in train:
        for words in sentence:
            word, tag = words
            trans[tag] = {}
            emission[tag] = {}
            tag_count.update({tag})

    # tags = a list of all distinct tag 
    tags = list(tag_count)          
    tag_len = len(tags)            
    for tag in tags:
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
                trans[tag][sentence[index + 1][1]] += 1
            if word not in emission[tag]:
                emission[tag][word] = 1
            else:
                emission[tag][word] += 1
    
    # soomthing initial, emission, trans and unseen using laplace = 0.00001
    unseen = {}
    for tag in tags:
        ini_len = len(list(initial))
        initial[tag] = np.log(initial[tag] / ini_len)   
        unseen[tag] = np.log( 0.00001 / (tag_count[tag] + 0.00001 * len(emission[tag])))
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
                    prob = (initial[tag] + emission[tag][word]) if word in emission[tag] else (initial[tag] + unseen[tag])                        
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
                        prob = (curr + emission[tag][word]) if word in emission[tag] else (curr + unseen[tag])
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

def viterbi_p2(train, test):
    '''
    TODO: implement the optimized Viterbi algorithm. This function has time out limitation for 3 mins.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words)
            E.g [[word1,word2...]]
    output: list of sentences with tags on the words
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
        hap[tag] = np.log(hap[tag] / ha_count)
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