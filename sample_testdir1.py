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

dirlist = [ 'reference/lambda', 'regex1.py', 'newdir/testfile_a.txt', 'reference/newsubdir/testfile_b.txt', 'reference/nd1/nd1_1/testfile_c.txt' ]

def checkfilename(dir):
     pathlist = []
     if re.search('/',dir):
         #print dir + " is a directory, need to check if the directory exists"
         pathlist = re.split('/',dir)
         isDIR = True
     else:
         isDIR = False
     return (isDIR,pathlist)

def examine(filename):

    (isDIR,pathlist) = checkfilename(filename)
    if isDIR:
        length = len(pathlist)-1
        filetoadd = filename
        for x in range(length):
            path = ''
            for i in range(length):
                path += pathlist[i] + '/'
            length = length -1

            # when adding a new filename, the cur path must exist in svn first.  
            # he can run svn add dir.  this will recursively add all the files in the new dir into svn.
            if not os.path.isdir(path):
                filetoadd = path
                next
            
            else:
                print path + " directory exist, only need to run rsync, and svn add * " + path
                next
                #filetoadd = filename

        print "rsync " + filetoadd
        print " svn add " + filetoadd

            
                           
    if not isDIR:
        print filename + " is not a directory.  only need to run rsync, and svn add " + filename
        print "rsync " + filename
        print " svn add " + filename
        #print "rsync(filename)"
        #print "syncGit2Svn(svncmd + " " + repo+filename, filename)"


        #for i in range(len(pathlist)-1):
        #    dirname += pathlist[i] + '/'
        #    print dirname

        #if not os.path.isdir(dirname):
        #    print dirname + " this directory does not exist, need to run rsync, then svn add of this  " + dirname
#                rsync(filename)
#                syncGit2Svn(svncmd + " " + SVN_DIR+repo+dirname, SVN_DIR+repo+dirname)
#            break
        #else:
        #    print dirname + " directory exist, only need to run rsync, and svn add " + filename
                
#                rsync(filename)
#                syncGit2Svn(svncmd + " " + repo+filename, repo+filename)
                #print dirname

    print

def main():
    for filename in dirlist:

        print filename
        examine(filename)


    exit(0)

if __name__ == '__main__':
    main()


