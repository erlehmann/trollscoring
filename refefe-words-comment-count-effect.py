#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scipy.stats import ttest_ind

from model import fefeModel, refefeModel
fefe = fefeModel('ts')
refefe = refefeModel('comments.tsv')
posts = fefe.posts[:1000]

def average(l):
    try:
        return float(sum(l))/float(len(l))
    except ZeroDivisionError:
        return 0

def posts_with_word(word):
    return [p for p in posts if word in p.text]

def posts_without_word(word):
    return [p for p in posts if word not in p.text]

def comment_count(posts):
    return [len(refefe[p.fefets]) for p in posts]

def comment_count_difference(word):
    """
    Returns the difference comments for articles that have
    a word and comments for articles that do not have a word.
    """
    count_with_word = comment_count(posts_with_word(word))
    count_without_word = comment_count(posts_without_word(word))
    average_with_word = average(count_with_word)
    average_without_word = average(count_without_word)
    delta = average_with_word - average_without_word
    try:
        t, p = ttest_ind(count_with_word, count_without_word)
    except ZeroDivisionError:
        t, p = float('NaN'), float('NaN')
    return delta, t, p

print '\t'.join(['word', 'delta', 't', 'p'])
for word in (':-)', 'Amis', 'Leute', 'Polizei', 'USA', 'Mann', \
                 'Deutschland', 'Geld', 'Daten', 'Internet', \
                 'Menschen', 'Geld', 'Piraten', 'Zeit', 'Jahren', \
                 'Welt', 'Artikel', 'Problem', 'NPD', 'Frauen'):
    delta, t, p = comment_count_difference(word)
    print '\t'.join([word, str(delta), str(t), str(p)])
