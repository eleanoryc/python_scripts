#!/usr/bin/python

#find the latest modified csv file

import os
import glob

mtime = lambda f: os.stat(os.path.join('./', f)).st_mtime
#print mtime
lsOutList = list(sorted(glob.glob(os.path.join('./', "*.csv")), key=mtime))
print (lsOutList)
#The last entry is the file we need
rptFileName = lsOutList[-1]
print rptFileName
