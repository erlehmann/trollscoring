#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

class refefeComment(object):
    def __init__(self, ts, fefets, nick, text, ip, censored):
        self.ts = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
        self.fefets = fefets
        self.nick = nick.decode('utf-8')
        self.text = text.decode('utf-8')
        self.ip = ip
        self.censored = bool(int(censored))

class refefeModel(object):
    def __init__(self, filename):

        with open(filename) as f:
            content = f.read()
            rows = [r.split('\t') for r in content.split('NULL\n')[1:]]
            self.comments = [refefeComment(
                    row[1], row[2], row[3], row[4], row[5], row[6],
                    ) for row in rows]
