#!/usr/bin/python


# open one file at a time, read it, and append contents to array.  
# When the line match with #SUMMARY, call the function to process line.
# Save the array to a temp file.

import glob
import re

def combineFiles (reportFile):
    with open(reportFile,'r') as rFileHandle:
         for line in rFileHandle:
             #print line.strip()

             if not line or line[0] == '#':
                continue
             result_regex = re.compile(r'\[(.*?)\]')
             matchObj = result_regex.match(line)
             if (matchObj):
                 reportType = matchObj.group(1)
                 if reportType == "SUMMARY":
     #               try:
      #                  summaryList = processSummary(line)
                     print line
             
             with open('combine.csv','w') as wFileHandle:
                   #hFileHandle.write(htmlEndTag)
                   wFileHandle.write(line)

def main():
    for f in glob.glob("*.csv"):
       #print(f)
       combineFiles(f)
    exit(0)


if __name__ == '__main__':
    main()
