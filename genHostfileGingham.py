"""
    This script will gather the list of estateids in Gingham based on the DC.  With each estateid, 
    it will generate a list of hosts is in ACTIVE state, as well as in FAILED state

    example of curl command to gets all the estateids for a dc: 
            https://gingham1-0-crz.data.sfdc.net/api/operations/estateids/ukb

    once it gets all the estateids, it will generate the list of hostnames of each estateids

    Where to run this script:  Gingham API could be accessed from local desktop, so this script can be run on desktop
    How to run it:  
         eg: to query all the estateids for sp1 in IA2
            $ python ./genHostfileGingham.py --dc ia2 --sp sp1
         eg: if the estateid is known, no need to supply the DC and SP information
            $ python ./genHostfileGingham.py --estatesid ia2.none.ia2.sam_report_collector,ia2.none.ia2.sec_scan
    

    Author Eleanor Cheung
    @contact: echeung@salesforce.com

    1.  based on the DC and SP and query the estatesids in Gingham API
    2.  get the hostnames and status for each estateid
    3.  extract the hostnames from json output
    4.  write the hostnames to a local file

    ? may need to exclude db hosts?
    ? cbatch, hub, mq, and proxy hosts are in ACTIVE state after the build, should they be excluded?
    
    TODO:  maybe user can have an option to submit the estateid only, no --sp, or --dc
          if estateid only, need to validate if the estateid exists or not   
 
"""

import subprocess
import json
import argparse,sys
import socket
import getpass
from subprocess import Popen,PIPE

def getEstatesId(dc,sp):

    curltemplate = 'curl https://gingham1-0-crz.data.sfdc.net/api/operations/estateids/{0}' 
    # for now, just hardcoded the dc value
    curl_cmd = curltemplate.format(dc) 

    output = subprocess.check_output(curl_cmd,shell=True) 
                              #stdin=subprocess.PIPE,
                              #stdout=subprocess.PIPE,
                              #stderr=subprocess.PIPE)
        #output = p.stdout.read()
        #print output

    json_string = json.loads(output)
    print type(json_string)
    #print json_string['message']

    estateids = []
    for n in json_string['message']:
        #print n['name']
        if sp in n:
            estateids.append(n)
    
    return estateids

def getHostlist(estateids):

    # run the curl command to get the status of each hosts from gingham
    # for each estateid, run curl https://gingham1-0-crz.data.sfdc.net/api/estates/status/
    # message['estate']['hostPlacementLocation'][rackname]['hosts']

    curl_gnghm_template = 'curl https://gingham1-0-crz.data.sfdc.net/api/estates/status/{0}'
   
    all_activehosts = []
    all_failedhosts = []
 
    for i in estateids:
        # get the json output for each estateid
        curl_gnghm_cmd = curl_gnghm_template.format(i)
        print curl_gnghm_cmd
        g_output = subprocess.check_output(curl_gnghm_cmd,shell=True) 
                              #stdin=subprocess.PIPE,
                              #stdout=subprocess.PIPE,
                              #stderr=subprocess.PIPE)
        #output = p.stdout.read()
        #print g_output

        dict = json.loads(g_output)
        #print dict

        racks = dict['message']['estate']['hostPlacementLocation']
#        print "racks " + str(racks)

        #print type(racks)

        # get the list of racknames
        racklist = []
        for rackname in racks:
            #print rackname, racks[rackname]
            #print rackname
            # create a racklist, containing the rack names of the dict
            racklist.append(rackname)

        #print racklist

        # create 2 lists for storing the active and failed hosts
        #activehosts = []
        #failedhosts = []

        for rack in racklist:
            activehosts = []
            failedhosts = []
            #print "rack " + str(type(rack))
            #print racks[rack]['hosts']

            hostlist = racks[rack]['hosts']
            #print "hostlist " + str(type(hostlist))
            #print "Rack: " + rack
            #print "Number of hosts: " + str(len(hostlist))

            #print "Hostnames: "
            for h in hostlist:
                #print type(h) -> dict
                #print h['name'], h['status']
                if h['status'] == 'ACTIVE':
                    activehosts.append(h['name'])
                else:
                    failedhosts.append(h['name'])
            all_activehosts.extend(activehosts)
            all_failedhosts.extend(failedhosts)

        #print("{0} ".format(h))

    for ah in sorted(all_activehosts): print("active: {0}".format(ah))
    for fh in all_failedhosts: print("failed: {0}".format(fh))

    return all_activehosts,all_failedhosts
        
def createHostfile(all_activehosts,all_failedhosts):

    ahostfile = open("activehostfile.txt","a")
    fhostfile = open("failedhostfile.txt","a")

    sortedahlist = sorted(all_activehosts)
    sortedfhlist = sorted(all_failedhosts)
    for ah in sortedahlist:
        ahostfile.write(ah+'\n')
    for fh in sortedfhlist:
        fhostfile.write(fh+'\n')

    print('The lists of active and failed hostnames are written to ./activehostfile.txt and failedhostfile.txt')


def main(argv=None):

    parser = argparse.ArgumentParser()
    parser.add_argument('--dc', help="dc")
    parser.add_argument('--sp', help="superpod")
    parser.add_argument('--estatesid', help="estatesid, can be commas separated")
    args=parser.parse_args()

    if len(sys.argv) <1:
        parser.print_help()
        parser.exit(1)

    if args.sp:
        sp = args.sp
    if args.dc:
        dc = args.dc
    
    if args.estatesid:
        estatesids = args.estatesid
        estatesidlist = estatesids.split(",")
    else:      
        estatesidlist = getEstatesId(dc,sp)

    for id in estatesidlist:
        print id

    allactivehosts,allfailedhosts = getHostlist(estatesidlist)

    createHostfile(allactivehosts,allfailedhosts)

if __name__ == '__main__':

    main()
