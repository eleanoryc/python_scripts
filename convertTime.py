#!/usr/bin/python

import sys
import argparse

def getReadableTime(millis):
    secs,millis=divmod(millis,1000)
    mins,secs=divmod(secs,60)
    hrs,mins=divmod(mins,60)
    return hrs,mins,secs,millis


def main():
    argv = sys.argv[1:]
    ArgParser = argparse.ArgumentParser()
    ArgParser.add_argument('-m','--millisec',help='enter millisecs to convert to readable time',required=True)
    args = ArgParser.parse_args(args=argv)

    if args.millisec:
        m = int(args.millisec)
        hrs,mins,secs,millis = getReadableTime(m) 
        print str(hrs) + " hrs " + str(mins) + " mins " + str(secs) + "." + str(millis) + " secs "
    exit(0)


if __name__ == '__main__':
    main()
