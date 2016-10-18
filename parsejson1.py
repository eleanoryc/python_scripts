import requests,json
from pprint import pprint

url = "https://imt.dmz.salesforce.com/api/v1/observers/reports/?provider=config-checker&instance=CS85"

response = requests.get(url, verify=False)
data = response.json()


for json_data in data:

    #pprint(json_data)

#    print "Here is the providerId:"
#    print json_data['provider']

#    print "Here is the pod name"
#    print json_data['instance']

    realdata = json_data['observations']

    for k in realdata:
        if realdata[k] == 'ALERT':
            print "\nObservations:"
            print realdata['checkerName']
            print realdata[k]

