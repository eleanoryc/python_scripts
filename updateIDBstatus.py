""" A script to update status of the FFX host

    Creator:  Eleanor Cheung

    Usage:  ./update-idb-status.py --host <fqdn> --status <status>

    validate hostnames
    validate status, ensure it's a valid status in IDB

    1. finding the buddy pair, if the host is cs25-ffx1-20-par, then buddy pair is cs25-ffx2-20-par
			       if the host is cs25-ffx2-20-par, then buddy pair is cs25-ffx1-20-par

    2. find out if the host is a ffx host, from the hostname
        - split the hostname, get the second field
	- check if it contains ffx
		get the last charactor 1, or 2
		now determine the buddy pair hostname and return it
    TODO:
    3. check the status of the buddy pair hostname

    4. return the status to enduser.  enduser needs to confirm before updating to idb

"""
import subprocess
import json
import argparse,sys

# write a function to validate if the host is a ffx host
# if yes, return the buddy pair hostname

def validateHost(hname):

    hname = hname.split('.')
    print hname
    if 'ffx' in hname[0]:
        hostarr = hname[0].split('-')
        cluster = hostarr[0]
        role = hostarr[1][0:-1]
        num = hostarr[1][-1]
        count = hostarr[2]
        dc = hostarr[3]
    else:
        print 'not a ffx host'
        exit(0)

    if num == '1':
        newnum = role + '2'
    elif num == '2':
        newnum = role + '1'
    buddypair = '-'.join([cluster,newnum,count,dc])

    print buddypair

def main(argv=None):

    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', help="fqdn")
#    parser.add_argument('--status', help="iDB status")
    args=parser.parse_args()

    if len(sys.argv) <2:
        parser.print_help()
        parser.exit(1)

    if args.hostname:
        hostname = args.hostname
        validateHost(hostname)
	# validate it's a ffx host, if yes, determine the buddy pair
        #hostname = hostname.split('.')

#	if 'ffx' in hostname[0]:
          
#            hostarr = hostname[0].split('-')
#            cluster = hostarr[0] 
#            role = hostarr[1]
#	    num = hostarr[1][-1]
#            count = hostarr[2]
#            dc = hostarr[3]
#        else:
#            print 'not a ffx host'
#            exit(0)

#        print'{} {} {} {} {}'.format(cluster,role,num,count,dc)  


if __name__ == '__main__':

    main()
