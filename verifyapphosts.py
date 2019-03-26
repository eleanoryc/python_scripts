"""
    The script will verify a list of Capadd app hosts in LB, by running netstat, or linebacker
    It will verify it's running from PR. If not, it will exit program.
    The output is written in STDOUT and a log file in the current dir,  netstat_<date>.log, or linebacker_<date>.log 
    (linebacker is a script recommended by SR to check the ENABLED_STATUS and AVAILABILITY_STATUS of a host in LB.)

    By default, the linebacker output will give the status for all the hosts in the LB pool. That includes the hosts 
    are already in production, and the capadd hosts.  Also, the output will list the IP address instead of the hostnames.
    With this script, the linebacker log will only contain the hosts in the input file.

    @Author Eleanor Cheung
    @contact: echeung@salesforce.com

    TODO:  
    -check the script is running from orch server

"""

import argparse,sys
import time
import socket
import re
import os
import getpass
import subprocess
from subprocess import Popen, PIPE

#def verifyOrchhost()
    #fqdn=socket.gethostname()
    #hostname=fqdn.split('.')[0]
    #hosttype=hostname..split('-')[1]
    # check if hosttype contains 'orch'.  if not, exit 
    #host_regex = re.compile(r'orch')
    #searchObj = host_regex.search(hosttype)
    #if (searchObj):
        #return True    
    #else:
        #return False

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

def checksite(pod):
    #PR or DR
    # run hostname, and extract the site from the hostname
    fqdn=socket.gethostname()
    hostname=fqdn.split('.')[0]
    cursite=hostname.split('-')[-1]
    #now have the pod and site from openfile(), can run inventory action command to check it's PR/DR
    # run inventory action command, assign the output to a variable
    inv_cmd = "inventory-action.pl -action read -resource cluster -cluster.name " + pod + " -use_krb_auth | grep -i DR"
    inv=subprocess.Popen(inv_cmd,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    result = inv.stdout.readlines()
    if result == []:
        error = inv.stderr.readlines()
        print >>sys.stderr, "ERROR: %s" % error
    else:
        print pod + str(result) 

    result_regex = re.compile(r'false')
    searchObj = result_regex.search(result[0])
    if (searchObj):
        print pod + " " + cursite + " is the PR.  Start verifying..."
    else:
        print pod + " " + cursite + " is the DR, exit program."
        sys.exit(0)

def getipaddress(hostlist):

    iphost_dict={}
    for h in hostlist:
        ip=socket.gethostbyname(h)
        iphost_dict[ip]=h
    return iphost_dict

def extracthostnames(ifile):

    # open file and put hostnames into a list
    # get the site, and pod from the input file
    # hostnames = [hostname.strip('\n').split(',') for hostname in open("test_hostname.txt", 'r').readlines()]
    with open(ifile) as f:
        hostnames = map(str.rstrip, f)
    pod=hostnames[0].split("-")[0]
    site=hostnames[0].split("-")[-1]

    return hostnames,pod,site

def executePoolManipulation(krb_user,krb_password,hostnames):
    command='sfdc_pool_manipulation.pl -u ' + krb_user + ' -i -s status -H ' 
    #print command
    #prompt='Enter current password for ' + krb_user + ':'

    for h in hostnames:
        host=h+":8085"
        command=command + h + ":8085"
        proc=subprocess.Popen(["sfdc_pool_manipulation.pl", "-u", "%s" % krb_user, "-i", "-s" ,"status", "-H", "%s" % host],
                          stdin=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          stdout=subprocess.PIPE)

        stdoutdata=proc.communicate(krb_password+'\n')[0]
        print stdoutdata

def executeLinebacker(krb_password,pod):
    # linebacker -a p_get -p PO_na37-pool
    mylist = []
    pool='PO_' + pod + '-pool'
    command='linebacker -a p_get -p ' + pool
    print "start running "  + command
    try:
        proc=subprocess.Popen(["linebacker", "-a", "p_get", "-p", "%s" % pool],
                     stdin=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     stdout=subprocess.PIPE)
    except OSError as e:
        print "OSError > ",e.strerror

    stdoutdata=proc.communicate(krb_password+'\n')[0]
      
    return stdoutdata

def processstdout(stdoutdata,iphost_dict,hostlist):

    newdata = re.sub("Password: ","",stdoutdata)
    timestamp = time.strftime('%Y%m%d%H%M%S')
    logfile='linebacker_' + timestamp + '.log'
    pattern=re.compile('^\[')
    i = 0
    obj={}

    #lines = [y for y in (x.strip() for x in stdoutdata.splitlines()) if y]
    lines = [y for y in (x.strip() for x in newdata.splitlines()) if y]

    for line in lines:
        # check if the line begin with [, then write to file
        newlist = False
        if re.match(pattern,line):
            newlist = True
        else:
            newlist = False

        if newlist is True:
            i = i + 1
            obj['l' + str(i)] = []
            obj['l' + str(i)].append(line+"\n")
        else:
            for key,value in iphost_dict.iteritems():
               if re.search(key,line):
                   newline = re.sub(key,value,line)+"\n"
                   obj['l' + str(i)].append(newline)
        next

    found = False
    notfoundlist = []

    for o in obj:
        for h in hostlist:
            hostpattern = re.compile(h)
            for l in obj[o]:
                if hostpattern.search(l):
                    found = True
                    break
                else:
                    found = False
                    continue
            if found is False:
                notfoundlist.append(h + " is not in LB \n")

            obj[o].extend(notfoundlist)
            notfoundlist = []

    with open(logfile,'w') as f_out:
        for o in obj:
            print "----------"
            f_out.write("----------\n")
            for i in obj[o]:
                print i,
                f_out.write(i)

def executeNetstat(hostnames,site):

    # define a list of leading edge DCs
    le_list = ['dfw','frf','hnd','iad','ord','par','phx','prd','ukb']
    timestamp = time.strftime('%Y%m%d%H%M%S')
    logfile='netstat_'+ timestamp + '.log'

    # leading edge has a different lb hostname vs trailing edge
    if site in le_list:
        egrep_cmd="egrep dcl[0-9]-" + site
    else:
        egrep_cmd="eqrep *bigip[0-9]-" + site

    netstat_cmd = "netstat -tapl | grep -i est | grep 8085 | " + egrep_cmd + " | wc -l"
    print "Start running " + netstat_cmd
    for h in hostnames:
        try:
            ssh=subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-o', 'ConnectTimeout=10', "%s" % h, netstat_cmd],
                          shell=False,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
        except (subprocess.CalledProcessError,subprocess.TimeoutExpired):
            print subprocess.TimeoutExpired

        netstatOutput = ssh.stdout.readlines()
        if netstatOutput == []:
            error = ssh.stderr.readlines()
            print >>sys.stderr, "ERROR: %s" % error
            with open(logfile,'a+') as logFileHandle:
                logFileHandle.write("ERROR: %s \n" % error)
        else:
            print h,netstatOutput[0].strip() + ' connections'
            with open(logfile,'a+') as logFileHandle:
                logFileHandle.write(h + ' ' + netstatOutput[0].strip() + ' connections' + '\n')
    logFileHandle.close()

def main(argv=None):

    parser = argparse.ArgumentParser()
    parser.add_argument('--ifile', help='input file contains list of hostnames to be verified')
    parser.add_argument('--vtype', help='netstat or linebacker')
    args=parser.parse_args()

    #verifyOrchhost()

    if len(sys.argv) < 1:
        parser.print_help()
        parser.exit(1)

    if args.ifile:
        ifile = args.ifile
        try:
            f = open(ifile)
        except IOError as err:
            print("Error: input file", ifile, err)
            exit(1)

        (hostlist,pod,site)=extracthostnames(ifile)

        # need to run kinit before running inventory cmd
        (krb_user,krb_password)=get_krb()
        mkinit(krb_user,krb_password)

        checksite(pod) 

        # ipaddress is used to filter the output of linebacker, and replace ipaddress with hostname
        iphost_dict=getipaddress(hostlist)

        #runRRcmd(hostnames,pod,sp,site)
        #executePoolManipulation(krb_user,krb_password,hostnames)
        #runNetstat(hostnames,site)

    # by default, run linebacker, if return value is true, run netstat right after
    stdoutdata=executeLinebacker(krb_password,pod)
    if stdoutdata:
        processstdout(stdoutdata,iphost_dict,hostlist)
        executeNetstat(hostlist,site)
    else:
        exit(0) # no stdoutdata from linebacker


    if args.vtype:
        global vtype
        vtype=args.vtype
        #if ( vtype != 'netstat' ) and ( vtype != 'PoolManiupulation' ) and ( vtype != 'linebacker' ):
        if ( vtype != 'netstat' ) and ( vtype != 'linebacker' ):
            parser.print_help()
            exit(1)
        if ( vtype == 'netstat' ):
            executeNetstat(hostlist,site)
#        if ( vtype == 'PoolManiupulation' ):
#            executePoolManipulation(krb_user,krb_password,hostnames)
        if ( vtype == 'linebacker' ):
            stdoutdata=executeLinebacker(krb_password,pod)
            processstdout(stdoutdata,iphost_dict,hostlist)

    exit(0)

if __name__ == '__main__':
    main()

