#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Dieses Programm hat das Ziel, die Medienkompetenz der Leser zu
# steigern. Gelegentlich packe ich sogar einen handfesten Buffer
# Overflow oder eine Format String Vulnerability zwischen die anderen
# Codezeilen und schreibe das auch nicht dran.

import socket
socket.setdefaulttimeout(5)

from sys import stdin, stdout

for row in stdin.readlines():
    ip_address = row.strip()
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
    except:
        hostname = None
    stdout.write('%s\t%s\n' % (ip_address, hostname))
    stdout.flush()
