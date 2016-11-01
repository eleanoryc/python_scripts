"""
    The script will parse JSON output of Config Checker and Smoke Tests
    It will display the check with status failed/skipped/error tests for Smoke Tests.
    It will display the check with status ALERTED for config checker.
    
    @Author Eleanor Cheung
    @contact: echeung@salesforce.com

    TODO:  support multiple pods - done
           generate HTML report - currently the output is display on the terminal - done
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
    divnum = 0

    #if rtype == 'smoketest':
    report = 'smoke-test'
    #statuslist = ['failed','error','skipped']
    # status, category, failure
    #field = 'category'
    #field = ['category','failure']

    for pod in p_list:
        content = ''
        content = """<table border=1 width="1100px"><tr><td bgcolor=#2ECCFA width="120px">Pod: </td><td bgcolor=#2ECCFA width="970px">""" + pod + """</td></tr>\n""" + """<tr><td valign=top width="120px">""" + report.title() + """:\n</td>"""
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
                        divnum += 1
                        hide, show = processdiv(divnum)
                        failtest += """<P>Category:  """ + realdata['category'] + """<br>Status:  """ + realdata[d] + """
                            <br>Owner: """ + realdata['owner'] +  """
                            <div> <a id=\"""" + hide + """\" href=\"#""" + hide + """\" class=\"hide\">+ Failure:</a> <a id=\"""" + show + """\" href=\"#""" + show + """\" class=\"show\">- message:</a> <div class=\"details\">  """ + realdata['failure'] + """</div>\n</div></P>""" 

                    if realdata[d] == 'error':
                        divnum += 1
                        hide, show = processdiv(divnum)
                        failtest += """<P>Category:  """ + realdata['category'] + """<br>Status:  """ + realdata[d] + """
                            <br>Owner: """ + realdata['owner'] +  """
                            <div> <a id=\"""" + hide + """\" href=\"#""" + hide + """\" class=\"hide\">+ Error:</a> <a id=\"""" + show + """\" href=\"#""" + show + """\" class=\"show\">- message:</a> <div class=\"details\">  """ + realdata['error'] + """</div>\n</div></P>""" 

                    if realdata[d] == 'skipped':
                        failtest += """<P>Category:  """ + realdata['category'] + """<br>Status:  """ + realdata[d] + """<br> Owner: """ + realdata['owner'] + """</P>"""


        content += """<td width="970px">""" + failtest + """</td></tr></table><br>\n"""
        failtest = ''
        #divnum = 0
        allcontent += content
    generatehtmlReport(allcontent,p_list)

def parseconfigchecker(p_list):
    global URL
    content = ''
    failtest = ''
    allcontent = ''
    divnum = 0

    #if rtype == 'configchecker':
    report = 'config-checker'
#    statuslist = ['ALERT']
        # state, checkerName, message
        #field = 'checkerName'
#    field = ['checkerName','message']

    for pod in p_list:
        content = ''
        content = """<table border=1 width=\"1100px\"><tr><td bgcolor=#2ECCFA width=\"120px\">Pod: </td><td bgcolor=#2ECCFA width=\"970px\">""" + pod + """</td></tr>\n""" + """<tr><td valign=top width=\"120px\">""" + report.title() + """:\n</td>"""
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
                        divnum += 1
                        hide, show = processdiv(divnum)
                        failtest += """<P>checkerName:  """ + realdata['checkerName'] + """ <br>state:  """ + realdata[d] + """ 
                               <div> <a id=\"""" + hide + """\" href=\"#""" + hide + """\" class=\"hide\">+ message:</a> <a id=\"""" + show + """\" href=\"#""" + show + """\" class=\"show\">- message:</a> <div class=\"details\">  """ + realdata['message'] + """</div>\n</div></P>"""

        content += """<td width=\"970px\">""" + failtest + """</td></tr></table><br>\n"""
        failtest = ''
        #divnum = 0
        allcontent += content
    generatehtmlReport(allcontent,p_list)

def processdiv(num):
    h = 'hide' + str(num)
    s = 'show' + str(num)
    return h, s

def generatehtmlReport(htmlContent,p_list):

# create a file for write in the current directory
# start writing with html open tab
# write content
# close the file when it's done
# output to the screen the location and name of the file
    allpods = ''
    htmlHeaderCSS = """<html><head>\n<STYLE TYPE=\"text/css\"><!--\n
    .details,
    .show,
    .hide:target {
       display: none;
    }
    .hide:target + .show,
    .hide:target ~ .details {
       display: block;
    }
    H3{font-family: verdana; font-size: 22pt;}\nTD{font-family: verdana; font-size: 10pt;}\n--->\n</STYLE>\n<body>"""

    for pod in p_list:
       allpods += pod + " "

    htmlTitle = "<H3>" + rtype.title() + " Report for " + allpods + "</H3>"
    htmlEndTag = "<br><br>\n</body>\n</html>"

    timestamp = time.strftime('%Y%m%d%H%M%S')
    htmlFileName = 'report' + timestamp + '.html'

    with open(htmlFileName,'w') as htmlFileHandle: 
        htmlFileHandle.write(htmlHeaderCSS)
        htmlFileHandle.write(htmlTitle)
        htmlFileHandle.write(htmlContent)
        htmlFileHandle.write(htmlEndTag)
        htmlFileHandle.close()

    cwd = os.getcwd()
    filename = cwd + '/' + htmlFileName
    print 'HTML Report:  ', filename

def main(argv=None):

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

    if args.rtype:
        global rtype
        rtype = args.rtype
        print rtype

        if ( rtype != 'configchecker' ) and ( rtype != 'smoketest' ):
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


