#!/usr/bin/python

import os
import sys


DIR='/Users/echeung/djfos'

try:
   os.chdir(DIR)
except OSError as e:
   print "File/directory : " + e.filename 
   print "Error msg: " + str(e.strerror) 
