#!/usr/bin/python

import sys
import argparse
# the .git2svn is the directory to store gitrepo, svn repo, and this script
sys.path.append("/home/echeung/.git2svn")
#import subprocess_2_7
import subprocess
import os
import pwd
import re

dirlist = [ 'reference/lambda', 'regex1.py', 'newdir/testfile_a.txt', 'reference/newsubdir/testfile_b.txt' ]

for l in dirlist:
    #print l
    if re.search('/',l):
        print "using search, it's a directory: " + l

    if os.path.isdir(l):
        print "it's a directory: " + l
    else:
        print "something " + l    


#recurse() {
# for i in $1/*; do
#    if [ -d "$i" ]; then
#        printf "dir: $i \n"
#        recurse "$i"
#    elif [ -f "$i" ]; then
#        printf "file: $i \n"
#    fi
# done
#}



