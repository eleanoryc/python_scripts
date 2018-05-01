#!/usr/bin/python

import re
import sys
from datetime import datetime, date, timedelta
from collections import Counter

parts = [
     r'(?P<mode>.*)',                   # mode
     r'(?P<user>.*)',                   # user
     r'(?P<comment>.*)',                # comment 
]

pattern = re.compile(r':'.join(parts)+r'\s*\Z')

# Regex for a feed request.
#feed = re.compile(r'/all-this/(\d\d\d\d/\d\d/[^/]+/)?feed/(atom/)?')

noofhit = 0

with open ("example.log", "r") as rFileHandle:
    for line in rFileHandle:

        m = pattern.match(line)
        hit = m.groupdict()
        if hit:
            noofhit += 1
        print hit


print noofhit


