#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chardet
import codecs
import csv
import sentiment

with open('refefe-10000+280.csv') as f:
    content = f.read()

rows = [' '.join(r.split()) for r in content.split('NULL')]
reader = csv.reader(rows, delimiter=';')
for row in reader:
    fefetimestamp = row[2]
    comment = row[4].decode('utf-8').encode('latin-1', 'replace')
    if comment is not None:
        mood = sentiment.sentiment(comment, 'de')
        print fefetimestamp, '\t', mood, '\t', comment
