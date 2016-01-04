#! /usr/bin/env python

# this is part of another script
# to find out if a directory exists in svn or not.
# if it does not, it will do "svn add" from the directory exists in svn

import os

Rootdir = '/Users/echeung/Documents/salesforce/'
filename = 'python_script/testdir/newdir/new/'

print filename
filetoadd = ''
for path_segment in filename.split('/'):

    if filetoadd:
        filetoadd += '/'
    filetoadd += path_segment
#    print "filetoadd: " + filetoadd
#    print "path_segment: " + path_segment

    if not os.path.isdir(Rootdir + filetoadd):
        print "svn add -q " + Rootdir + filetoadd
#        # We found the first segment in the path that isn't an existing folder
        break
