#!/usr/bin/env python
# -*- coding: utf-8 -*-

from html5lib import parse
from os import path, walk
from datetime import datetime
from werkzeug.contrib.cache import FileSystemCache

ts_cache = FileSystemCache('.ts_cache', threshold=99999999, \
                               default_timeout=99999999)
text_cache = FileSystemCache('.text_cache', threshold=99999999, \
                                 default_timeout=99999999)

with open('all.rdns.tsv') as f:
    rdns = {
        token[0]:token[1][:-1] for token in \
            (line.split('\t') for line in f.readlines())
        }

# see <http://stackoverflow.com/questions/8733233/filtering-out-certain-bytes-in-python#answer-8735509>
def valid_XML_char_ordinal(i):
    return 0x20 <= i <= 0xD7FF or i in (0x9, 0xA, 0xD) or \
        0xE000 <= i <= 0xFFFD or 0x10000 <= i <= 0x10FFFF

def sanitize(string):
    return ''.join(c for c in string if valid_XML_char_ordinal(ord(c)))

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
        tree = parse(sanitize(self.html), 'lxml')
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
        text = text_cache.get(self.fefets)
        if text == None:
            tree = parse(sanitize(self.html), 'lxml')
            text = tree.xpath('string()')
            text_cache.set(self.fefets, text)
        return text

    @property
    def ts(self):
        ts = ts_cache.get(self.fefets)
        if ts == None:
            ts =  datetime.fromtimestamp(int(self.fefets, base=16) \
                                             ^ 0xFEFEC0DE)
            ts_cache.set(self.fefets, ts)
        return ts

class fefeModel(object):
    def __init__(self, directory):
        self.posts = [fefePost(directory, timestamp) for timestamp in \
                          (filename for filename in \
                               list(walk(directory))[0][2])]

    def __getitem__(self, fefets):
        return [p for p in self.posts if p.fefets == fefets][0]
