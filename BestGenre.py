#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 14:50:48 2020

@author: Tom
"""
import GetOldTweets3 as got
import nltk
from nltk.corpus import stopwords

#Takes a music genre and returns a list of tweets that mention it
def GetTweets(genre,maxTweets = 3):
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(genre)\
                                           .setMaxTweets(maxTweets).setTopTweets(True).setSince("2015-01-01")
    return got.manager.TweetManager.getTweets(tweetCriteria)

#Takes a single tweet and extracts the adjectives
def AdjExtract(tweet):
    adj_list = []
    POS_tags = ['JJ','JJR','JJS','PDT','RB','RBR','RBS']
    tokens = nltk.word_tokenize(tweet.text)
    tags = nltk.pos_tag(tokens)
    
    for i in range(len(tags)):
        word = tags[i][0]
        tag  = tags[i][1]
    
        if tag in POS_tags:
            adj_list.append(word)
        else:
            pass
        i += 1
    return adj_list

#Takes a single word and returns a polarity score
    
def AdjScore(word):
    global p_score
    p_score = 0
    word = "=" + word.lower()+" "
    with open("subjclueslen1-HLTEMNLP05.tff") as infile:
        for line in infile:
            if word in line: 
                if (line[5] == 's') and ('negative' in line):
                    p_score = -1
                    #print(word,p_score)
                    break
                elif line[5] == 's' and 'positive' in line:
                    p_score = 1
                    #print(word,p_score)
                    break
                elif line[5] == 'w' and 'negative' in line:
                    p_score = -0.2
                    #print(word,p_score)
                    break
                elif line[5] == 'w' and 'positive' in line:
                    p_score = 0.2
                    #print(word,p_score)
                    break
            else:
                pass
        return p_score
    
def GenreScore(genre):
    adjectives = []
    clean_adjs=[]
    score = 0
    scored_adjs = 0
    tweets = GetTweets(genre,100)
    for tweet in tweets:
        adjectives.append(AdjExtract(tweet))
    for tweet in adjectives:
        for word in tweet:
            polarity = AdjScore(word)
            score += polarity
            if polarity != 0:
                scored_adjs += 1
                clean_adjs.append(word)
    score = score / scored_adjs *100
    return (score,clean_adjs)

def WordCount(clean_adjs):
    sw = stopwords.words('english')
    clean_tokens = clean_adjs
    for token in clean_adjs:
        if token in sw:
            clean_tokens.remove(token)
    freq = nltk.FreqDist(clean_tokens)
    freq.plot(20, cumulative=False)
    


                                       
genres = ["classical","pop","rock","jazz","country","hip hop","EDM","rap"]

for genre in genres:
    print(genre+" gets a score of " + str(int(GenreScore(genre+" music")[0]))+'%')

