#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chardet
import codecs
import csv

import socket
socket.setdefaulttimeout(5)

from sys import stdout

with open('refefe.csv') as f:
    content = f.read()

rows = [' '.join(r.split()) for r in content.split('NULL')]
reader = csv.reader(rows, delimiter=';')
for row in reader:
    ip_address = row[5].decode('utf-8').encode('latin-1', 'replace')
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
    except:
        hostname = None
    stdout.write('%s\t%s\n' % (ip_address, hostname))
    stdout.flush()
