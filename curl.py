#!/usr/bin/python

import re
import sys
import subprocess
import getopt

HOSTS = [ "ops-rhel64-1-dev", "ops-rhel64-2-dev" ]
CURLCMD="curl -s -o /dev/null -w "%{http_code}" https://api.opentok.com/"

for HOST in HOSTS:
   ssh = subprocess.Popen(["ssh", "%s" % HOST, CURLCMD],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
   result = ssh.stdout.readlines()

if result == []:
    error = ssh.stderr.readlines()
    print >>sys.stderr, "ERROR: %s" % error
else:
    print result




