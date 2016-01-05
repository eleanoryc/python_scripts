#!/usr/bin/python

# script will take portPattern and split it into individual ports
# portPattern can be consisted of port range, and single port


import re

portPattern = '{2001-5000},80,443,8001'
portList = []

# remove the "{", "}", if any
portPattern = re.sub("\{|\}", '', portPattern)

# for every ',' separated token, only '-' is the non numeric char allowed
for portRange in (portPattern.split(",")):
    portRange = portRange.strip()
    if "-" in portRange:
        rangeList = portRange.split("-")
        if (len(rangeList)) > 2:
            logger.error ("Invalid port range" + portPattern)
            exit(1)
        # if port range is specified, take only the start and the end port alone
        # ie, if it is 8869-8889, then take only 8869 and 8889
        portList.append(rangeList[0])
        if (len(rangeList)) == 2:
            portList.append(rangeList[1])
    else:
        if re.search(r'\D', portRange):
            logger.error("Invalid port Range" + portPattern)
            exit(1)
        portList.append(portRange)

print portList
