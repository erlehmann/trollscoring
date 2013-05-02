#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chardet
import codecs

from sys import stdout

with open('all.rdns.tsv') as f:
    rdns = {
        token[0]:token[1][:-1] for token in \
            (line.split('\t') for line in f.readlines())
        }

from model import refefeModel
m = refefeModel('comments.tsv')

for comment in m.comments:
    if comment.censored:
        continue
    ip_address = comment.ip
    try:
        hostname = rdns[ip_address]
    except KeyError:
        hostname = 'domain.invalid'
    stdout.write('%s\t%s\n' % (ip_address, hostname))
    stdout.flush()
