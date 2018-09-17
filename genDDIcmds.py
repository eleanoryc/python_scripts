"""
    This script will run the /usr/local/bin/rackbotquery.py command against each host in the
    the hostfile given by the user.
    The output of racbotquery.py will have the information of IB address in a json format.
    The end result is to generate the ddi command to add the ib address for each host.

    where to run:  ops0-sysmgt host

    echo "ddi_cmds.txt" | mailx -s "ddi_cmds" -a "./ddi_cmds.txt" 

    #Author Eleanor Cheung
     @contact: echeung@salesforce.com

    DONE:  take 1 argument from user, a file with a list of shorthostnames
    DONE:  write the ddi commands to a file

"""

import subprocess
import json
import argparse,sys

#hostlist = ['shared0-samminioniot1-8-ia2', 'shared0-samminioniot1-9-ia2']
#rackbotquery_cmd = '/usr/local/bin/rackbotquery.py host shared0-samminioniot1-8-ia2'

# sample output of rackbotquery.py
#{
#    "shared0-samminioniot1-9-ia2.ops.sfdc.net": {
#        "hostname": "shared0-samminioniot1-9-ia2.ops.sfdc.net", 
#        "ip_address": "10.227.149.90", 
#        "ib_ip_address": "10.217.8.204", 
#        "idb_cluster": "IA2-SAM_IOT", 
#        "idb_superpod": "NONE", 
#        "serial": "GXR1CM2"
#    }
#}

ddcmdtemplate = "ddi add a {0}.ops.sfdc.net {1} --allow-duplicates \n"

def processHlist(hostlist):

    for h in hostlist:
        rackbotquery_cmd = '/usr/local/bin/rackbotquery.py host ' + h
        output = subprocess.check_output(rackbotquery_cmd,shell=True) 
                              #stdin=subprocess.PIPE,
                              #stdout=subprocess.PIPE,
                              #stderr=subprocess.PIPE)
        #output = p.stdout.read()
        #print output

        json_string = json.loads(output)
        #print type(json_string)
        #print json_string
        IB_address = json_string[h+'.ops.sfdc.net']['ib_ip_address']

        #print 'ddi add a ' + h + '.ops.sfdc.net ' + IB_address + ' --allow-duplicates'
        #ddi_cmd = 'ddi add a ' + h + '.ops.sfdc.net ' + IB_address + ' --allow-duplicates' + "\n"
        ddi_file = open("ddi_commands.txt", "a")
        ddi_file.write(ddicmdtemplate.format(h,IB_address))

    ddi_file.close

def main(argv=None):

    parser = argparse.ArgumentParser()
    parser.add_argument('--hostfile', help="hostlist shortname")
    args=parser.parse_args()

    if len(sys.argv) <1:
        parser.print_help()
        parser.exit(1)

    if args.hostfile:
        hostfile = args.hostfile
        # read the hostfile, and put it in a hostlist
        with open(hostfile) as f:
            hostlist = map(str.rstrip,f)
            
        processHlist(hostlist)

if __name__ == '__main__':

    main()
