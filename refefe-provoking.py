#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

from collections import Counter

from model import fefePost, refefeModel
m = refefeModel('comments.tsv')

comment_count = Counter()
for ts in [c.fefets for c in m.comments if not c.censored]:
    comment_count[ts] += 1

articles_with_word = Counter()
comments_for_word = Counter()
for ts in comment_count:
    post = fefePost('ts', ts)
    article_words = set(post.html.split())
    for word in article_words:
        comments_for_word[word] += comment_count[ts]
        articles_with_word[word] += 1

provoking_words = Counter()
for word in articles_with_word:
    provoking_words[word] = \
        (comments_for_word[word] / articles_with_word[word]) * \
        (1 - (1 / articles_with_word[word]))  # paranoid margin of error

print provoking_words.most_common(100)
