"""
    The script will parse JSON output of Config Checker and Smoke Tests
    It will display the check with status failed/skipped/error tests for Smoke Tests.
    It will display the check with status ALERTED for config checker.
    
    @Author Eleanor Cheung
    @contact: echeung@salesforce.com

    TODO:  support multiple pods - done
           generate HTML report - currently the output is display on the terminal
           send report to email address
"""

import argparse,sys
import requests,json
from pprint import pprint

URL = 'https://imt.dmz.salesforce.com/api/v1/observers/reports/?provider='

def parsereport(rtype,p_list):
    global URL
    content = ''
    failtest = ''
    allcontent = ''

    if rtype == 'configchecker':
        report = 'config-checker'
        statuslist = ['ALERT']
        field = 'checkerName'
    if rtype == 'prodtest':
        report = 'smoke-test'
        statuslist = ['failed','error','skipped']
        field = 'category'

    for pod in p_list:
        content = ''
        content = "<tr><td>Pod: </td><td>" + pod + "</td></tr>\n" + "<tr><td>" + report + ":\n</td>"
        print pod, report, ":"

        rURL = URL + report + '&instance=' + pod
        print 'URL:', rURL
        response = requests.get(rURL, verify=False)
        data = response.json()
        if not data:
            print pod, ' has no report for ' + report + ' in IMT'
#            exit(0)
            content += "<td>" + pod + " has no report for " + report + " in IMT\n</td></tr>"
            failtest = ''
            next
        for json_data in data:
#            pprint(json_data)
            realdata = json_data['observations']
            for k in realdata:
                for status in statuslist:
                    if realdata[k] == status:
                        #print realdata[k], ': ' ,realdata[field]
                        # create an variable and assign the content to it
                        #failtest +=  "<td>something" + realdata[k] + ": " + realdata[field] + "</td></tr>\n"
                        failtest +=  "something" + realdata[k] + ": " + realdata[field] + "<br>"
        content += "<td>" + failtest + "</td></tr>\n"
        print 'Content:'
        print content
        #allcontent += content
        allcontent += content
    generatehtmlReport(allcontent)

def generatehtmlReport(htmlContent):

# create a file for write in the current directory
# start writing with html open tab
# write content
# close the file when it's done
# output to the screen the location and name of the file
    htmlHeader = "<html>\n<STYLE TYPE=\"text/css\">\n<!--\nTD{font-family: verdana; font-size: 10pt;}\n--->\n</STYLE>\n<body>"
    htmlTableOpen = "<table border=1>"
    htmlTableClose = "</table>"
    htmlEndTag = "<br><br>\n</body>\n</html>"
    htmlFileName = 'content.html'
    with open(htmlFileName,'w') as htmlFileHandle: 
        htmlFileHandle.write(htmlHeader)
        htmlFileHandle.write(htmlTableOpen)
        htmlFileHandle.write(htmlContent)
        htmlFileHandle.write(htmlTableClose)
        htmlFileHandle.write(htmlEndTag)
        htmlFileHandle.close()



def main(argv=None):

    #url = "https://imt.dmz.salesforce.com/api/v1/observers/reports/?provider="

    parser = argparse.ArgumentParser()
    parser.add_argument('--rtype', help="configchecker or prodtest")
    parser.add_argument('--pods', help="specify the instances (comma separated)")
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


