#!/usr/bin/python

import sys
import getopt


def usage():
   print 'usage:  argument.py -i <inputfile>'

def main(argv):
   inputfile = ''
   if len(sys.argv) <= 1:
      usage()
      exit(1)

   try:
      opts, args = getopt.getopt(argv,"hi:",["ifile="])
   except getopt.GetoptError:
      print 'usage:  argument.py -i <inputfile>'
      sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
         usage()
         #print 'usage:  argument.py -i <inputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
         print 'Input file is', inputfile

if __name__ == "__main__":
   main(sys.argv[1:])
