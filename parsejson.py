"""
    The script will parse JSON output of Config Checker and Smoke Tests
    display the failed tests.
    
    @Author Eleanor Cheung
    @contact: aru@salesforce.com

"""

import argparse,sys
import requests,json
from pprint import pprint

URL = 'https://imt.dmz.salesforce.com/api/v1/observers/reports/?provider='

def parsereport(rtype,p_list):
    global URL
    if rtype == 'configchecker':
        report = 'config-checker'
        checklist = ['ALERT']
        field = 'checkerName'
    if rtype == 'prodtest':
        report = 'smoke-test'
        checklist = ['failed','error','skipped']
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
                for check in checklist:
                    if realdata[k] == check:
                        print realdata[k], ': ' ,realdata[field]
        print

#def configchecker(p_list):
#    global URL
#    for pod in p_list:
#        ccURL = URL + 'config-checker' + '&instance=' + pod
#        #URL += 'config-checker' + '&instance=' + pod.upper()
#        print ccURL
#        response = requests.get(ccURL, verify=False)
#        data = response.json()
#        if not data:
#            print pod, ' has no report for ConfigChecker in IMT'
##            exit(0)
#            next
#        for json_data in data:
##            pprint(json_data)
#            realdata = json_data['observations']
#            for k in realdata:
#                if realdata[k] == 'ALERT':
#                    print realdata[k], ': ' ,realdata['checkerName']

#def prodtest(p_list):
#    global URL
#    for pod in p_list:
#        ptURL = URL + 'smoke-test' + '&instance=' + pod
#        #URL += 'config-checker' + '&instance=' + pod
#        print ptURL

#        response = requests.get(ptURL, verify=False)
#        data = response.json()
#        if not data:
#            print pod, ' has no report for Prodtest in IMT'
##        exit(0)
#        for json_data in data:
#
#            realdata = json_data['observations']
#            for k in realdata:
#                if (realdata[k] == 'error') or (realdata[k] == 'skipped') or (realdata[k] == 'failed'):
#                    print realdata[k], ': ' ,realdata['category']

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
#        if rtype == 'configchecker':
#            #url += 'config-checker' + '&instance=' + pod
#            configchecker(p_list)             
#        if rtype == 'prodtest':
#            #url += 'smoke-test' + '&instance=' + pod
#            prodtest(p_list) 

    exit(0)

if __name__ == '__main__':
    main()


