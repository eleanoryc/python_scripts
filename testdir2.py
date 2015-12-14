#! /usr/bin/env python

import os
import re

filename = '/Users/echeung/Documents/salesforce/python_script/testdir/newdir'

pathlist = []
if re.search('/',filename):
    pathlist = re.split('/',filename)

    length = len(pathlist)-1
    filetoadd = filename
    path = ''
    for i in range(length):
        path += pathlist[i] + '/'
        length = length -1

    if not os.path.isdir(path):
    #    print path + " does not exist"
        filetoadd = path
        next
    else:
     #   print "nothing" 
        next
   
    print " path to add: " + filetoadd
