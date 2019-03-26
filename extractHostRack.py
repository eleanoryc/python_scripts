"""   # a simple script to read the yaml file, and parse the data
      the interest is to extract the list of hosts in the yaml file
      the yaml file has simple structure as the following,
      / ipRange: {}
      / roles: {}
      / racks: 
      /  subnet:
      /  hosts: []

    @Author Eleanor Cheung
    @contact: echeung@salesforce.com

    Example to run: python ./extractHostRack.py --pattern cs93 --estatefile cs93-app_main.yaml

    --estatefile , it can be any yaml file in estates
    --pattern  , it does not limit to podname only, it can be part of a hostname in the yaml file

"""

import yaml
import argparse,sys
import os

def genHostRackDict(estatefile):

    # Parse the yaml file and assign to a dictionary
    with open(estatefile, 'r') as ifile:
        dict=yaml.load(ifile)

# sample estate file
# {'ipRange': '10.222.198.64/26', 'roles': {'dapp': 1, 'app': 10, 'cbatch': 4}, 'racks': {'c13-9a': {'subnet': '10.222.198.64/29', 'hosts': ['cs16-app1-1-iad.ops.sfdc.net', 'cs16-app1-2-iad.ops.sfdc.net', 'cs16-cbatch1-1-iad.ops.sfdc.net']}, 'g10-9a': {'subnet': '10.222.198.80/29', 'hosts': ['cs16-app1-4-iad.ops.sfdc.net', 'cs16-app1-5-iad.ops.sfdc.net', 'cs16-cbatch1-2-iad.ops.sfdc.net']}, 'c05-9a': {'subnet': '10.222.198.88/29', 'hosts': ['cs16-app2-2-iad.ops.sfdc.net', 'cs16-app2-5-iad.ops.sfdc.net']}, 'b12-9a': {'subnet': '10.222.198.72/29', 'hosts': ['cs16-app2-1-iad.ops.sfdc.net', 'cs16-app2-3-iad.ops.sfdc.net', 'cs16-cbatch2-1-iad.ops.sfdc.net']}, 'b13-9a': {'subnet': '10.222.198.96/29', 'hosts': ['cs16-app2-4-iad.ops.sfdc.net', 'cs16-cbatch2-2-iad.ops.sfdc.net']}, 'f04-9a': {'subnet': '10.222.198.104/29', 'hosts': ['cs16-app1-3-iad.ops.sfdc.net', 'cs16-dapp1-1-iad.ops.sfdc.net']}}}


    # racks is a dict containing the racks and subnets and hosts, (extracted from dict['rack'], value of 'racks' in dict)
    rackdict = dict['racks']

    # create an empty list to store the names of racks
    racklist = []

    for rackname in rackdict:
        # create a racklist, containing the rack names of the dict
        racklist.append(rackname)

    tmphostlist = []

    # create a dict to store hostname and rack
    hostdict = {}

    for rack in racklist:

        if 'hostGroups' in rackdict[rack]:
            for h in rackdict[rack]['hostGroups']:
                tmphostlist.extend(h['hosts'])

                for host in tmphostlist:
                    hostdict[host] = rack

            tmphostlist = []

        else:
            tmphostlist.extend(rackdict[rack]['hosts'])

            for host in tmphostlist:
                hostdict[host] = rack

            tmphostlist = []

    return hostdict

def getHostRackInfo(hostdict,pattern):

    for key in sorted(hostdict.iterkeys()):
        if pattern in key:
            #print "%s: %s" % (key, "ops-cnc"+hostdict[key])
            print "%s: %s" % (key, hostdict[key])
        else:
            next

def main(argv=None):

    parser = argparse.ArgumentParser()
    parser.add_argument('--pattern', help='pattern, eg: na35')
    parser.add_argument('--estatefile', help='estatefile, eg: iad-ffx.yaml')
    #parser.add_argument('--estates', help='estates, eg: ffx')
    #parser.add_argument('--range', help='range, eg. 1-15')
    args=parser.parse_args()

    if len(sys.argv) < 1:
        parser.print_help()
        parser.exit(1)

    if args.pattern:
        pattern = args.pattern
        print "%s: %s" % ("Pattern", pattern)

    if args.estatefile:
        estatefile = args.estatefile
        print "%s: %s" % ("Estate file", estatefile)

    hostrackdict = genHostRackDict(estatefile)
    getHostRackInfo(hostrackdict,pattern)

if __name__ == '__main__':
    main()

