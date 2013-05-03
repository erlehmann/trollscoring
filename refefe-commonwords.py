#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
c = Counter()

from model import refefeModel
m = refefeModel('comments.tsv')

from sys import stdout

with open('top100de.utf8.txt') as f:
    common_words = [word.strip().decode('utf-8') for word in f.readlines()]

for sentence in (comment.html for comment in m.comments):
    for word in sentence.split():
        if (word[0].upper() != word[0]) or (len(word) == 1) or \
                (word.lower() in common_words):
            continue
        c[word] += 1

for word, count in c.most_common(100):
    stdout.write('%s\t%s\n' % (count, word))
