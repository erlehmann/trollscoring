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
    def __init__(self, ts, fefets, nick, html, ip, censored):
        self.ts = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
        self.fefets = fefets
        self.nick = nick.decode('utf-8')
        self.html = html.decode('utf-8')
        self.ip = ip
        try:
            self.hostname = rdns[ip]
        except KeyError:
            self.hostname = None
        self.censored = bool(int(censored))

    @property
    def text(self):
        tree = parse(self.html, 'lxml')
        return tree.xpath('string()')

class refefeModel(object):
    def __init__(self, filename):
        with open(filename) as f:
            content = f.read()
            rows = [r.split('\t') for r in content.split('NULL\n')[1:]]
            self.comments = [refefeComment(
                    row[1], row[2], row[3], row[4], row[5], row[6],
                    ) for row in rows]

    def __getitem__(self, fefets):
        return [c for c in self.comments if c.fefets == fefets]

class fefePost(object):
    def __init__(self, directory, fefets):
        self.fefets = fefets
        try:
            with open(path.join(directory, fefets)) as f:
                self.html = f.read().strip().decode('utf-8')
        except IOError:
            self.html = ''

    @property
    def text(self):
        tree = parse(self.html, 'lxml')
        return tree.xpath('string()')

    @property
    def ts(self):
        return datetime.fromtimestamp(int(self.fefets, base=16) ^ 0xFEFEC0DE)

class fefeModel(object):
    def __init__(self, directory):
        self.posts = [fefePost(directory, timestamp) for timestamp in \
                          (filename for filename in \
                               list(walk(directory))[0][2])]

    def __getitem__(self, fefets):
        return [p for p in self.posts if p.fefets == fefets][0]
