"""
    The script will parse JSON output of Config Checker and Smoke Tests
    It will display the check with status failed/skipped/error tests for Smoke Tests.
    It will display the check with status ALERTED for config checker.
    
    @Author Eleanor Cheung
    @contact: echeung@salesforce.com

    TODO:  support multiple pods - done
           generate HTML report - currently the output is display on the terminal - in progress
           send report to email address
"""

import argparse,sys
import requests,json
import time
import os
from pprint import pprint

URL = 'https://imt.dmz.salesforce.com/api/v1/observers/reports/?provider='

def parsesmoketest(p_list):
    global URL
    content = ''
    failtest = ''
    allcontent = ''

    #if rtype == 'smoketest':
    report = 'smoke-test'
    #statuslist = ['failed','error','skipped']
    # status, category, failure
    #field = 'category'
    #field = ['category','failure']

    for pod in p_list:
        content = ''
        content = """<table border=1 width="1100px"><tr><td bgcolor=#2ECCFA width="120px">Pod: </td><td bgcolor=#2ECCFA width="970px">""" + pod + """</td></tr>\n""" + """<tr><td valign=top width="120px">""" + report + """:\n</td>"""
        print pod, report, ":"

        rURL = URL + report + '&instance=' + pod
        print 'URL:', rURL
        response = requests.get(rURL, verify=False)
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
                for d in realdata:
                    if realdata[d] == 'failed':
                        failtest += """<P>Status:  """ + realdata[d] + """<br>Category:  """ + realdata['category'] + """<br> Failure:  """ + realdata['failure'] + """<br> Owner: """ + realdata['owner'] + """</P>"""
                    if realdata[d] == 'error':
                        failtest += """<P>Status:  """ + realdata[d] + """<br>Category:  """ + realdata['category'] + """<br> Error:  """ + realdata['error'] + """<br> Owner: """ + realdata['owner'] + """</P>"""
                    if realdata[d] == 'skipped':
                        failtest += """<P>Status:  """ + realdata[d] + """<br>Category:  """ + realdata['category'] + """<br> Owner: """ + realdata['owner'] + """</P>"""

                #for k in realdata.keys():
                #    if k == 'failed':
                #        failtest += "<P>" + k + ":  "+ realdata[k] + "<br>Category:  " + realdata['category'] + "<br> Failure:  " + realdata['failure'] + "</P>"
                #    if k == 'error':
                #        failtest += "<P>" + k + ":  " + realdata[k] + "<br>Category:  " + realdata['category'] + "<br> Error:  " + realdata['error'] + "</P>"
                #    if k == 'skipped':
                #        failtest += "<P>" + k + ":  " + realdata[k] + "<br>Category:  " + realdata['category'] + "</P>"

        content += """<td width="970px">""" + failtest + """</td></tr></table><br>\n"""
        failtest = ''
#        print 'Content:'
#        print content
        allcontent += content
    generatehtmlReport(allcontent,p_list)

def parseconfigchecker(p_list):
    global URL
    content = ''
    failtest = ''
    allcontent = ''
    divnum = 0
    hide = 'hide'
    show = 'show'

    #if rtype == 'configchecker':
    report = 'config-checker'
#    statuslist = ['ALERT']
        # state, checkerName, message
        #field = 'checkerName'
#    field = ['checkerName','message']

    for pod in p_list:
        content = ''
        content = """<table border=1 width="1100px"><tr><td bgcolor=#2ECCFA width="120px">Pod: </td><td bgcolor=#2ECCFA width="970px">""" + pod + """</td></tr>\n""" + """<tr><td valign=top width="120px">""" + report + """:\n</td>"""
        print pod, report, ":"

        rURL = URL + report + '&instance=' + pod
        print 'URL:', rURL
        response = requests.get(rURL, verify=False)
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
                for d in realdata:
                    if realdata[d] == 'ALERT':
                        #failtest += """<P>state:  """ + realdata[d] + """<br>checkerName:  """ + realdata['checkerName'] + """<br> message:  """ + realdata['message'] + """</P>"""

                        divnum += 1
                        hide += str(divnum)
                        show += str(divnum)
                        #failtest += """<P>state:  """ + realdata[d] + """<br>checkerName:  """ + realdata['checkerName'] + """<br> 
                        #       <div> <a id=\" """ + hide + """\" href=\"# """ + hide + """\" class=\"hide\">+ message:</a> <a id=\" """ + show + """\" href=\"# """ + show + """\" class=\"show\">- message:</a> <div class=\"details\">  """ + realdata['message'] + """</div>\n</div></P>"""

                        failtest += """<P>state:  """ + realdata[d] + """<br>checkerName:  """ + realdata['checkerName'] + """<br> 
                               <div> <a id=\"""" + hide + """\" href=\"#""" + hide + """\" class=\"hide\">+ message:</a> <a id=\"""" + show + """\" href=\"#""" + show + """\" class=\"show\">- message:</a> <div class=\"details\">  """ + realdata['message'] + """</div>\n</div></P>"""

                        hide = 'hide'
                        show = 'show'

        content += """<td width="970">""" + failtest + """</td></tr></table><br>\n"""
        failtest = ''
        divnum = 0
        #print 'Content:'
        #print content
        allcontent += content
    generatehtmlReport(allcontent,p_list)

def generatehtmlReport(htmlContent,p_list):

# create a file for write in the current directory
# start writing with html open tab
# write content
# close the file when it's done
# output to the screen the location and name of the file
    allpods = ''
    htmlHeader = """<html><head>\n<STYLE TYPE=\"text/css\"><!--\n
    .details,
    .show,
    .hide:target {
       display: none;
    }
    .hide:target + .show,
    .hide:target ~ .details {
       display: block;
    }
    H3{font-family: verdana; font-size: 20pt;}\nTD{font-family: verdana; font-size: 10pt;}\n--->\n</STYLE>\n<body>"""

    for pod in p_list:
       allpods += pod + " "
    htmlTitle = "<H3> Report for " + allpods + "</H3>"
    #htmlTableOpen = "<table border=1>"
    #htmlTableClose = "</table>"
    htmlEndTag = "<br><br>\n</body>\n</html>"
    timestamp = time.strftime('%Y%m%d%H%M%S')
    htmlFileName = 'report' + timestamp + '.html'
    with open(htmlFileName,'w') as htmlFileHandle: 
        htmlFileHandle.write(htmlHeader)
        htmlFileHandle.write(htmlTitle)
        htmlFileHandle.write(htmlContent)
     #   htmlFileHandle.write(htmlTableClose)
        htmlFileHandle.write(htmlEndTag)
        htmlFileHandle.close()

    cwd = os.getcwd()
    filename = cwd + '/' + htmlFileName
    print 'HTML Report:  ', filename

def main(argv=None):

    #url = "https://imt.dmz.salesforce.com/api/v1/observers/reports/?provider="

    parser = argparse.ArgumentParser()
    parser.add_argument('--rtype', help="configchecker or smoketest")
    parser.add_argument('--pods', help="specify the instances (comma separated)")
    parser.add_argument('--email', help="email address (comma separated)")
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
        if ( rtype == 'configchecker' ):
            parseconfigchecker(p_list)
        if ( rtype == 'smoketest' ):
            parsesmoketest(p_list)
        #parsereport(rtype,p_list)
 

    exit(0)

if __name__ == '__main__':
    main()


