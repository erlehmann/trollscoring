#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylab

from collections import Counter
from matplotlib import ticker

from model import refefeModel
refefe = refefeModel('comments.tsv')
comments = [c for c in refefe.comments if str(c.hostname) != 'None' and \
                not c.censored]

hostnames = Counter(['.'.join(str(c.hostname).split('.')[-2:]) \
                         for c in comments])

def plot(hostnames):
    labels, values = zip(*sorted(hostnames, key=lambda x: x[1]))
    pylab.clf()
    fig = pylab.figure(figsize=(8,8))
    pylab.suptitle = ('Häufige ')

    ax = fig.add_subplot(1,1,1)
    ticks = range(len(labels))
    ax.set_yticks(ticks)
    ax.set_yticklabels(labels)

    ax.set_xscale('log')
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

    bar = pylab.barh(ticks, values, color=['#000000'], align='center')
    pylab.gcf().subplots_adjust(left=0.4)
    pylab.show()

plot(hostnames.most_common(20))

uni_hostnames = Counter(['.'.join(str(c.hostname).split('.')[-2:]) \
                         for c in comments \
                         if 'fh-' in c.hostname or \
                         'rwth-' in c.hostname or \
                         'uni-' in c.hostname or \
                         'hu-berlin' in c.hostname
                     ])

plot(uni_hostnames.most_common(20))
