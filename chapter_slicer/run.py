import json
import multiprocessing
import os
import urllib.request
import urllib
import re
from multiprocessing import Process
from multiprocessing.pool import Pool
from urllib import request

def FindChapter(content):
    pattern = re.split('<h[12345]>\n?.+\n?</h[12345]>',content)
    if len(pattern)<=2:
        return "None"
    return pattern

if __name__ == "__main__":
    f = open('tag.json')
    data = json.load(f)
    s = 0
    t = 0
    for i in data.keys():
        name = 'raw_data/f'+ i + '.html'
        print(s,t)
        print(name, )
        t += 1
        try:
            book = open(name,encoding='utf-8').read()
        except:
            book = open(name,encoding='ISO8859-1').read()

        span = FindChapter(book)
        if span == "None":
            s += 1
        print(span)
