"""
    The script will parse JSON output of Config Checker and Smoke Tests
    It will display the check with status failed/skipped/error tests for Smoke Tests.
    It will display the check with status ALERTED for config checker.
    
    @Author Eleanor Cheung
    @contact: echeung@salesforce.com

"""

import argparse,sys
import requests,json
from pprint import pprint

URL = 'https://imt.dmz.salesforce.com/api/v1/observers/reports/?provider='

def parsereport(rtype,p_list):
    global URL
    if rtype == 'configchecker':
        report = 'config-checker'
        statuslist = ['ALERT']
        field = 'checkerName'
    if rtype == 'prodtest':
        report = 'smoke-test'
        statuslist = ['failed','error','skipped']
        field = 'category'

    for pod in p_list:
        print pod, report, ":"
        rURL = URL + report + '&instance=' + pod
        print 'URL:', rURL
        response = requests.get(rURL, verify=False)
        data = response.json()
        if not data:
            print pod, ' has no report for ConfigChecker in IMT'
#            exit(0)
            next
        for json_data in data:
#            pprint(json_data)
            realdata = json_data['observations']
            for k in realdata:
                for status in statuslist:
                    if realdata[k] == status:
                        print realdata[k], ': ' ,realdata[field]
        print

def main(argv=None):

    #url = "https://imt.dmz.salesforce.com/api/v1/observers/reports/?provider="

    parser = argparse.ArgumentParser()
    parser.add_argument('--rtype', help="configchecker or prodtest")
    parser.add_argument('--pods', help="specify the instance")
    args=parser.parse_args()

    if len(sys.argv) < 4:
        parser.print_help()
        parser.exit(1)

    if args.pods:
        pod_list = args.pods
        p_list = pod_list.upper().split(",")
#        print type(p_list)

    if args.rtype:
        rtype = args.rtype
        print rtype
        if ( rtype != 'configchecker' ) and ( rtype != 'prodtest' ):
            parser.print_help()
            exit(1)
        parsereport(rtype,p_list)

    exit(0)

if __name__ == '__main__':
    main()


