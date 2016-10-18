#!/usr/bin/python

import os
import sys
import getopt


def usage(exitstatus=None):
    cmdname=os.path.basename(sys.argv[0])
    print "Usage: %s [-h] [-i|--ifile] [-o|--ofile] [-e|--elist]" % (cmdname)
    #print 'usage:  argument.py -i <inputfile> -o <outputfile> -e <emaillist>'

    if exitstatus != None:
        sys.exit(exitstatus)

def main(argv):
   inputfile = ''
   outputfile = ''
   email = ''
   if len(sys.argv) <= 1:
      usage(1)

   try:
      opts, args = getopt.getopt(argv,"hi:o:e:",["ifile=","ofile=","elist="])
   except getopt.GetoptError:
      usage(1)

   for opt, arg in opts:
      if opt in ("-h","--help"):
         usage(0)
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-e", "--elist"):
         elist = arg
         email = elist.split(',')
         print email
   print 'Input file is', inputfile
   print 'Output file is', outputfile
   print 'Email recipiant is', email

if __name__ == "__main__":
   main(sys.argv[1:])
