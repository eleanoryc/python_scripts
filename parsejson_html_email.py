"""
    The script will parse JSON output of Config Checker and Smoke Tests
    It will display the check with status failed/skipped/error tests for Smoke Tests.
    It will display the check with status ALERTED for config checker.
    
    @Author:  Eleanor Cheung
    @contact: echeung@salesforce.com

    TODO:  support multiple pods - done
           generate HTML report - done
           send report to email address - in progress
           not in user story, send the report to IMT?
    nice to have:   setup postfix locally for testing
                    add a feature to have access to JSON file, check 
"""

import argparse,sys
import requests,json
import time
import datetime
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
        content = "<table border=1><tr><td bgcolor=#2ECCFA>Pod: </td><td bgcolor=#2ECCFA width=700>" + pod + "</td></tr>\n" + "<tr><td valign=top>" + report + ":\n</td>"
        print pod, report, ":"

        rURL = URL + report + '&instance=' + pod
        print 'URL:', rURL

        ## try and except, if able to get the JSON file, exit with error if failed
        try:
            response = requests.get(rURL, verify=False)
        except requests.exceptions.RequestException as err:
            print err
            print("check if you're SFM Auth")
            sys.exit(1)
           

        data = response.json()
        if not data:
            print pod, ' has no report for ' + report + ' in IMT'
#            exit(0)
            failtest += pod + " has no report for " + report + " in IMT<br>"
            next
        else:
            for json_data in data:
#                pprint(json_data)
                realdata = json_data['observations']
                for k in realdata:
                    for status in statuslist:
                        if realdata[k] == status:
                            failtest +=  realdata[k] + ": " + realdata[field] + "<br>"
            failtest += "<P>For detail of each fail tests, please check <br> URL: " + '<a href="' + rURL + '">here</a>'  + "</a></P>"
        content += "<td>" + failtest + "</td></tr></table><br>\n"
        failtest = ''
        print 'Content:'
        print content
        allcontent += content
    generatehtmlReport(allcontent)

def generatehtmlReport(htmlContent):

# create a file for write in the current directory
# start writing with html open tab
# write content
# close the file when it's done
# output to the screen the location and name of the file
    htmlHeader = "<html>\n<STYLE TYPE=\"text/css\">\n<!--\nTD{font-family: verdana; font-size: 10pt;}\n--->\n</STYLE>\n<body>"
    htmlEndTag = "<br><br>\n</body>\n</html>"
    timestamp = time.strftime('%Y%m%d%H%M%S')
    htmlFileName = 'report' + timestamp + '.html'
    with open(htmlFileName,'w') as htmlFileHandle: 
        htmlFileHandle.write(htmlHeader)
        htmlFileHandle.write(htmlContent)
        htmlFileHandle.write(htmlEndTag)
        htmlFileHandle.close()

    print 'file:  ', htmlFileName
    sendEmail(htmlFileName) 

def sendEmail(htmlReport):

    # send email and attach the report
    # need to know the name of the report

    # cat $resultFilename| uuencode $resultFilename | mailx -s "$INPUTPOD validation on $INPUTSITE ran by $CURUSER on bastion $bastionSITE" $INPUTEMAIL
    # uuencode htmlReport | mailx -s "" EMAIL_LIST

    global EMAIL_ERROR_MESSAGES
    global EMAIL_SUMMARY_MESSAGES

    print "The report is sent to ", EMAIL_LIST 
    email_msg = content
    print email_msg
    email_sub = "The report for "
    email_sub = """ " """ + email_sub + """  " """
    email_cmd = "mailx -s %s %s <<<'%s' " % (email_sub, EMAIL_LIST, email_msg)
    try:
        subprocess.check_call(email_cmd,shell=True)
        logger.info("Email is sent to " + EMAIL_LIST)
        EMAIL_ERROR_MESSAGES = ""
        EMAIL_SUMMARY_MESSAGES = ""
    except subprocess.CalledProcessError as e:
        print("Exception Cmd : "  + str(e.cmd))
        print("Cmd Return Code : " +  str(e.returncode))
        ##### log this error
        logger.error("Exception Cmd : "  + str(e.cmd))
        logger.error("Exception Output : '" +  str(e.output) + "'")


def main(argv=None):

    #url = "https://imt.dmz.salesforce.com/api/v1/observers/reports/?provider="

    parser = argparse.ArgumentParser()
    parser.add_argument('--rtype', help="configchecker or prodtest")
    parser.add_argument('--pods', help="specify the instances (comma separated)")
    parser.add_argument('--email_list', help="email address (comma separated)")
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

    global EMAIL_LIST
    if args.email_list:
        EMAIL_LIST = args.email_list

    exit(0)

if __name__ == '__main__':
    main()


