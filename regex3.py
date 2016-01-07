#!/usr/bin/python

# print lines are not empty line or begins with #

import re

regexline = re.comile('^#|^\s*$')

with open('testfile.txt','r') as rFile:
    for l in rFile:
        if no regexline.search(l):
            print l

