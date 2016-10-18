"""
    The script will parse JSON output from Config Checker and Smoke Tests
    extract the failed tests.
    
    @Author Eleanor Cheung
    @contact: aru@salesforce.com

"""

import argparse,sys
import requests,json
from pprint import pprint

def configchecker(url,pod):
    print url
    response = requests.get(url, verify=False)
    data = response.json()
    if not data:
        print pod, ' has no data'
        exit(0)

    for json_data in data:
#        pprint(json_data)
        realdata = json_data['observations']
        for k in realdata:
            if realdata[k] == 'ALERT':
                print realdata[k], ': ' ,realdata['checkerName']

def prodtest(url,pod):
    response = requests.get(url, verify=False)
    data = response.json()
    if not data:
        print pod, ' has no data'
        exit(0)
    for json_data in data:

        realdata = json_data['observations']
        for k in realdata:
            if (realdata[k] == 'error') or (realdata[k] == 'skipped'):
                print realdata[k], ': ' ,realdata['category']

def main(argv=None):

    url = "https://imt.dmz.salesforce.com/api/v1/observers/reports/?provider="

    parser = argparse.ArgumentParser()
    parser.add_argument('--rtype', help="configchecker or prodtest")
    parser.add_argument('--pod', help="specify the instance")
    args=parser.parse_args()

    if len(sys.argv) < 4:
        parser.print_help()
        parser.exit(1)

    if args.pod:
        pod = args.pod.upper()

    if args.rtype:
        rtype = args.rtype
        if ( rtype != 'configchecker' ) and ( rtype != 'prodtest' ):
            parser.print_help()
            exit(1)
        if rtype == 'configchecker':
             url += 'config-checker' + '&instance=' + pod
             configchecker(url,pod)             
        if rtype == 'prodtest':
             url += 'smoke-test' + '&instance=' + pod
             prodtest(url,pod) 

    exit(0)

if __name__ == '__main__':
    main()


