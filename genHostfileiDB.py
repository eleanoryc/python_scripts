"""
    This script will run curl command to get the list of hosts for the PODGROUP in PROVISIONING status
    giving the cluster.clusterType = POD,
               cluster.operationalStatus = ACTIVE, HW_PROVISIONING, PRE_PRODUCTION, PROVISIONING
               host.operationalStatus = ACTIVE, or PROVISIONING

    example of the curl command:  curl --tlsv1.2 --negotiate -u: "https://cfg0-idbapik1-0-ia2.data.sfdc.net/api/1.04/hosts?cluster.superpod.dataCenter.name=IA2&cluster.clusterType=POD&cluster.operationalStatus=HW_PROVISIONING&operationalStatus=PROVISIONING&fields=name"

    where to run:  ops0-sysmgt host

    Author:  Eleanor Cheung
    @contact:  echeung@salesforce.com

    USAGE:  python ./getHostlistiDB.py --hoststatus <hoststatus> --clusterstatue <clusterstatus>
       eg:  python ./genHostfileiDB.py --hoststatus ACTIVE --clusterstatus HW_PROVISIONING

    1.  prompt user for kerberos password
    2.  get the dc info and insert in the curl command
    3.  run curl command
    4.  extract the hostnames from json output
    5:  write the hostnames to a local file

    DONE: do a checking of the status, exit or print error if the status doesn't match
    DONE: exclude db hosts?
    TODO:  check the hostfile.  if the hostfile exists, either rename it, or empty it
    ? cbatch, hub, mq, and proxy hosts are in ACTIVE state after the build
 
"""

import subprocess
import json
import argparse,sys
import socket
import getpass
from subprocess import Popen,PIPE

def get_krb():
    #prompt user to enter kerberos password
    krb_user = getpass.getuser()
    krb_password = getpass.getpass(prompt="Kerberos Password: ")
    return krb_user,krb_password

def mkinit(krb_user,krb_password):
    kinit = '/usr/bin/kinit'
    kinit_args = [ kinit, '%s' % (krb_user) ]
    kinit = Popen(kinit_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    kinit.stdin.write('%s\n' % krb_password)
    kinit.wait()

def extractdc():

    fqdn=socket.gethostname()
    hostname=fqdn.split('.')[0]
    dc=hostname.split('-')[-1]
    return dc

def runCURL(dc,hoststatus,clusterstatus):

    curltemplate = 'curl --tlsv1.2 --negotiate -u: \"https://cfg0-idbapik1-0-{0}.data.sfdc.net/api/1.04/hosts?cluster.superpod.dataCenter.name={1}&cluster.clusterType=POD&cluster.operationalStatus={2}&operationalStatus={3}&fields=name\"' 
    curl_cmd = curltemplate.format(dc,dc.upper(),clusterstatus.upper(),hoststatus.upper()) 

    print curl_cmd

    output = subprocess.check_output(curl_cmd,shell=True) 
                              #stdin=subprocess.PIPE,
                              #stdout=subprocess.PIPE,
                              #stderr=subprocess.PIPE)
        #output = p.stdout.read()
        #print output

    json_string = json.loads(output)
    #print type(json_string)
    #print json_string['data']

    hostlist = []
    for n in json_string['data']:
        #print n['name']
        # excluding db hosts
        if not 'db' in n:
            hostlist.append(n['name'])
        #for skey,value in n.iteritems():
        #    print key, value
    
    return hostlist

def createHostfile(hostlist):
    # if hostfile.txt exists, overwrite it, w
    hostfile = open("hostfile.txt","w")

    sortedhlist = sorted(hostlist)
    for h in sortedhlist:
        hostfile.write(h+'\n')

    return(True)
    #print('The list of hostnames is written to ./hostfile.txt')


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--hoststatus', help="hoststatus, eg: ACTIVE" )
    parser.add_argument('--clusterstatus', help="clusterstatus, eg: ACTIVE,PROVISIONING,PRE_PRODUCTION")
    args=parser.parse_args()

    if len(sys.argv) <1:
        parser.print_help()
        parser.exit(1)

    if args.hoststatus:
        # validate host status, ACTIVE,PROVISIONING
        hstatus = ['ACTIVE','PROVISIONING']
        hoststatus = args.hoststatus.upper()
        if not hoststatus in hstatus:
            print('please give valid host status, ACTIVE, or PROVISIONING')
            exit(1)

    if args.clusterstatus:
        # validate cluster status, ACTIVE,PROVISIONING,PRE_PRODUCTION
        cstatus = ['ACTIVE','PROVISIONING','PRE_PRODUCTION','HW_PROVISIONING']
        clusterstatus = args.clusterstatus.upper()
        if not clusterstatus in cstatus:
            print('please give valid cluster status, ACTIVE, HW_PROVISIONING, PROVISIONING or PRE_PROUCTION')
            exit(1)

    # prompt user for kerberos password
    (krb_user,krb_password)=get_krb()
    mkinit(krb_user,krb_password)

    dc = extractdc()

    # run the curl command to get the hostlist
    hostlist = runCURL(dc,hoststatus,clusterstatus)
    #print hostlist

    # write to a hostfile
    if createHostfile(hostlist):
        print('The list of hostnames is written to ./hostfile.txt')


if __name__ == '__main__':

    main()

