#!/usr/bin/env python
# -*- coding: utf-8 -*-

from html5lib import parse
from os import path, walk
from datetime import datetime

with open('all.rdns.tsv') as f:
    rdns = {
        token[0]:token[1][:-1] for token in \
            (line.split('\t') for line in f.readlines())
        }

class refefeComment(object):
    def __init__(self, ts, fefets, nick, text, ip, censored):
        self.ts = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
        self.fefets = fefets
        self.nick = nick.decode('utf-8')
        self.text = text.decode('utf-8')
        self.ip = ip
        try:
            self.hostname = rdns[ip]
        except KeyError:
            self.hostname = None
        self.censored = bool(int(censored))

class refefeModel(object):
    def __init__(self, filename):
        with open(filename) as f:
            content = f.read()
            rows = [r.split('\t') for r in content.split('NULL\n')[1:]]
            self.comments = [refefeComment(
                    row[1], row[2], row[3], row[4], row[5], row[6],
                    ) for row in rows]

class fefePost(object):
    def __init__(self, directory, ts):
        self.ts = ts
        with open(path.join(directory, ts)) as f:
            self.html = f.read().strip()

    @property
    def text(self):
        tree = parse(self.html, 'lxml')
        return tree.xpath('string()')

class fefeModel(object):
    def __init__(self, directory):
        self.posts = [fefePost(directory, timestamp) for timestamp in \
                          (filename for filename in \
                               list(walk(directory))[0][2])]
