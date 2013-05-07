#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from pylab import clf, hist, plot_date, savefig, subplots_adjust, suptitle, xticks

from model import fefeModel, refefeModel

print 'Loading fefe model …'
fefe = fefeModel('ts')

print 'Loading refefe model …'
refefe = refefeModel('comments.tsv')

print 'Filtering posts …'
#refefe_start = fefe['b3e52a2c'].ts
#posts = [p for p in fefe.posts[0:200] if p.ts > refefe_start]
posts = [p for p in fefe.posts if \
             int(p.fefets, base=16) ^ 0xFEFEC0DE > 1293675250L]

print 'Sorting posts …'
posts = sorted(posts, key=lambda x: x.ts)

print 'Collecting timestamps …'
X = [p.ts for p in posts]

def plot_save(X, Y, title, filename):
    clf()
    xticks(rotation=90)
    suptitle(title)
    subplots_adjust(bottom=0.2)
    plot_date(X, Y, 'k.')
    savefig(filename, dpi=600)

def hist_save(X, title, filename, bins=15):
    clf()
    suptitle(title)
    hist(X, histtype='stepfilled', color='k', bins=bins)
    savefig(filename, dpi=600)

from matplotlib.dates import date2num, num2date
def time_of_day(date):
    # see <http://stackoverflow.com/questions/4790265/plot-time-of-day-vs-date-in-matplotlib#answer-4795353>
    return num2date(date2num(date) % 1 + 1000)

print 'Calculating blog times …'
blog_times = [time_of_day(p.ts)\
    for p in posts]
plot_save(X, blog_times, u'Blogzeiten', 'fefe-blog-times.png')
hist_save([t.hour for t in blog_times], u'Blogzeiten', 'fefe-blog-times-hist.png', bins=24)

from itertools import chain

print 'Calculating comment times …'
comment_times = [[c.ts for c in refefe[fefets]] \
    for fefets in [p.fefets for p in posts]]
comment_times = list(chain(*comment_times))
comment_times_of_day = [[time_of_day(c.ts) for c in refefe[fefets]] \
    for fefets in [p.fefets for p in posts]]
comment_times_of_day = list(chain(*comment_times_of_day))

plot_save(comment_times, comment_times_of_day, u'Kommentarzeiten', 'refefe-comment-times.png')

print 'Calculating comment count …'
comment_count = [len(refefe[fefets]) \
         for fefets in [p.fefets for p in posts]]
plot_save(X, comment_count, u'Anzahl Kommentare', 'refefe-comment-count.png')
hist_save(comment_count, u'Anzahl Kommentare', 'refefe-comment-count-hist.png')

def average(values):
    try:
        return sum(values) / len(values)
    except ZeroDivisionError:
        return 0

print 'Calculating average comment lengths …'
average_comment_length = [average([len(c.text) for c in refefe[fefets]]) \
         for fefets in [p.fefets for p in posts]]

plot_save(X, average_comment_length, u'Durchschnittliche Kommentarlänge', 'refefe-average-comment-length.png')

print 'Calculating number of censored comments …'
censored_count = [sum([1 for c in refefe[fefets] if c.censored]) \
         for fefets in [p.fefets for p in posts]]

plot_save(X, censored_count, u'Anzahl zensierter Kommentare', 'refefe-censored-comments.png')

# TODO: schimpfwörter nach kommentar-position (ab wieviel prozent)
# TODO: wie viel datengewinn bringen komprimierte kommentare?
