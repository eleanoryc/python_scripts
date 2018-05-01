#!/usr/bin/python

import re
import sys
from datetime import datetime, date, timedelta
from collections import Counter

parts = [
     r'(?P<host>\S+)',                   # host %h
     r'\S+',                             # indent %l (unused)
     r'(?P<user>\S+)',                   # user %u
     r'\[(?P<time>.+)\]',                # time %t
     r'"(?P<request>.*)"',               # request "%r"
     r'(?P<status>[0-9]+)',              # status %>s
     r'(?P<size>\S+)',                   # size %b (careful, can be '-')
#     r'"(?P<referrer>.*)"',              # referrer "%{Referer}i"
#     r'"(?P<agent>.*)"',                 # user agent "%{User-agent}i"
]

pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')

# Regex for a feed request.
#feed = re.compile(r'/all-this/(\d\d\d\d/\d\d/[^/]+/)?feed/(atom/)?')


with open ("sampleapache.log", "r") as rFileHandle:
    for line in rFileHandle:

        m = pattern.match(line)
        hit = m.groupdict()

        print hit

