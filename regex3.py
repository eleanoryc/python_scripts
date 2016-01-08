#!/usr/bin/python

# print lines are not empty line or begins with #

import re

regexline = re.compile('^#|^\s*$')
with open('testfile.txt','r') as rFile:
    for l in rFile:
        if not regexline.search(l):
            print l.strip()


### or
print
with open('testfile.txt','r') as rFile:
    for l in rFile:
        if not re.search(r'^#|^\s*$',l):
            print l.strip()

