# !/usr/bin/env python
from __future__ import print_function

# usage: get the script to local and make sure you have python installed;
# python -m pdb /Users/snallagatla/DA/lic8.py --podname eu11,na8


"""
host_list.py:
- pass the podgroup and superpods or podnames
- get all the hosts names
- writes *_mandr_host.output, *_gabba_host.output in tmp/inventory/invhosts/{kingdom} directory
"""
__copyright__ = 'Copyright (c) 1999 - 2017, Salesforce.com, San Francisco, CA, All rights reserved.'
__author__ = 'Sudhakar Nallagatla'
__maintainer__ = 'Rick Feldmann'
__email__ = 'snallagatla@salesforce.com'
__status__ = 'Production'
__version__ = '1.0'

import json
import subprocess
import sys
import argparse
import re


def parse_json(json_data):
    """
    parse the returned json gets the required values
    :param json_data: bulk jsn data
    :return: pod name, dr status, dc name
    """
    # print(json_data.get("pods"))
    return [{
        'podname': json_data.get("pods")[i]['name'],
        'Primary': json_data.get("pods")[i]['dr'],
        'datacenter': json_data.get("pods")[i]['datacenter']
    } for i in range(len(json_data.get("pods")))]


def getpodname():
    """
    get all the pod names
    :return:
    """
    query = "https://podtap.internal.salesforce.com/connpool"
    proc = subprocess.Popen(["curl", "-sb -H", query], stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    json_data = json.loads(out)
    podcount = len(json_data.get("pods"))
    if podcount > 0:
        podname = parse_json(json_data)
    return podname


def processquery(pname="", datacenter="", primary=""):
    """
    Connects to connection pool and process the give query
    :param pname: pod name/s
    :param datacenter: kingdom name
    :param primary: If primary then false , later we switch false to true
    :return:
    """
    query = "https://podtap.internal.salesforce.com/connpool?pod=" + pname
    proc = subprocess.Popen(["curl", "-sb -H", query], stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    json_data = json.loads(out)
    # jj['results']
    sub1 = json_data.get("results")
    count = 0
    falsecount = 0

    for i in range(len(sub1)):
        try:
            Tr = json_data.get("results")[i]["pool_member"]
            # Right now intrested only app and sapp (SR pods) roles
            if Tr:
                if "-app" in json_data.get("results")[i]["host"] or "-sapp" in json_data.get("results")[i]["host"]:
                    count = count + 1
            else:
                if "-app" in json_data.get("results")[i]["host"] or "-sapp" in json_data.get("results")[i]["host"]:
                    falsecount = falsecount + 1
            hostname = json_data.get("results")[i]["host"]
            # print(hostname)
        except KeyError:  #
            print("Can't get the {} pod status".format(pname))
            break
    if primary:
        primary = "False"
    elif not primary:
        primary = "True"
    if count > 0 and falsecount == 0:
        print(
        "Podname:{0: <5} Pr:{1: <5} DC:{2: <5}  traffichosts:{3: <5} ".format(pname, primary, datacenter, count, ))
    elif falsecount > 0 and count == 0:
        print(
            "Podname:{0: <5} Pr:{1: <5} DC:{2: <5}  Nontraffichosts:{3: <5} ".format(pname, primary, datacenter,
                                                                                     falsecount, ))
    elif count > 0 and falsecount > 0:
        print(
            "Podname:{0: <5} Pr:{1: <5} DC:{2: <5}  traffichosts:{3: <5}  Nontraffichosts:{4: <5}".format(pname,
                                                                                                          primary,
                                                                                                          datacenter,
                                                                                                          count,
                                                                                                          falsecount))


def get_args():
    """
    Get the arguments from command line
    :return: podgroup name, superpod name, pod names
    """
    parser = argparse.ArgumentParser(
        description='Get the podgoup ')
    parser.add_argument('--podnames', "-podnames",
                        help='Ex: --podnames EU1,EU8 ', required=False)
    args = vars(parser.parse_args())

    # Convert everything to hyphen delimiter
    if args['podnames']:
        podnames = re.sub(r'([^\s\w]|_)+', ',', args['podnames'])
    else:
        podnames = ""
    return podnames


def main():
    """
    main function which run all the mention functions
    :return:
    """
    retcode = 0
    try:
        pnames = get_args()
        if pnames:
            plist = pnames.split(",")
            plist = [element.lower() for element in plist]
            for i in range(len(plist)):
                processquery(plist[i])
        else:
            totalplist = getpodname()
            for i in range(len(totalplist)):
                processquery(totalplist[i]['podname'], totalplist[i]['datacenter'], totalplist[i]['Primary'], )
    except:
        print ("Unknown exception is occurred, please refer the below stack trace:")
        return -1
    return retcode


if __name__ == "__main__":
    retcode = main()
sys.exit(retcode)


