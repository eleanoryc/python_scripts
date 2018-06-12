#!/usr/bin/python

#  ./generate_input_file.py -i inputfile -o outputfile
#  sample of inputfile
#  la4-lapp{1,2}-{1-8}-was
#  la4-lapp{1,2}-{1-8}-chi
#  this will read inputfile line by line
#  take the regex and expand them
#  write to an outputfile



import re
import sys
import getopt

def main(argv):
   inputfile = ''
   try:
      opts, args = getopt.getopt(sys.argv[1:],"h:i:o:")
   except getopt.GetoptError:
      print 'generate_input_file.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'generate_input_file.py -i <inputfile>'
         sys.exit()
      elif opt == '-i':
         inputfile = arg
      elif opt == '-o':
         outputfile = arg
   print 'Input file is ', inputfile
   print 'Output file is ', outputfile

   iFile = open(inputfile, 'r')
   oFile = open(outputfile, 'w')

   for line in iFile:
      m = re.match(r"(\w+\-\w+){(\d+),(\d+)}-{(\d+)-(\d+)}-(\w+)", line)
      instance = m.group(1)
      clusterBeg = m.group(2)
      clusterEnd = m.group(3)
      hostBeg = m.group(4)
      hostEnd = m.group(5)
      location = m.group(6)

      for i in range(int(clusterBeg), int(clusterEnd)+1):
         for j in range(int(hostBeg), int(hostEnd)+1):
            newline = '%s%d-%d-%s\n' % (instance,i,j,location)
            oFile.write(newline)

if __name__ == "__main__":
   main(sys.argv[1:])
