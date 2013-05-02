#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import get, post

def translate(text, sourcelang, targetlang):
    request = get(
        'http://mymemory.translated.net/api/get',
        params={
            'q': text,
            'langpair': '%s|%s' % (sourcelang, targetlang)
        }
    )
    return request.json[u'matches'][0][u'translation']

def sentiment(text, language):
    translated_text = translate(text, language, 'en')
    request = post(
        'http://text-processing.com/api/sentiment/',
        data={'text': translated_text}
    )
    if request.json is not None:
        return request.json['label']

if __name__ == '__main__':
    print sentiment('Der Schuldige an der Berliner S-Bahn-Misere ist gefunden. Thilo Sarrazin. Na das passt ja mal wieder...', 'de')
    print sentiment('Die Unterschicht frisst Müll, so einfach ist das!', 'de')
