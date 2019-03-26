# read ifile
# generate the subject line and description of the LB user stories
# version 2.  The input file will contain all the hostnames including the DCs
# eg.  na35-app1-21-dfw
# version 1. the input file does not contain the dc in the hostnames
# eg. na35-app1-21


import argparse
import sys

def create_description(ifile):

    content0 = 'Host List:\n\n'
    desc = ''
    firstlist=[]
    secondlist=[]

    with open(ifile) as f:
        hostnames = map(str.rstrip, f)
    pod = hostnames[0].split("-")[0]
    desc = desc + content0

# need to extract the dc off the hostname
# separate the hostlist into 2 lists, one list for each site

    # sort the list of hostnames first, hostnames.sort()
    hostnames.sort()

    # getting the value of dc from the first hostnames
    dc = hostnames[0].split("-")[-1]

    for h in hostnames:
        if dc == h.split("-")[-1]:
            dc1 = dc
            firstlist.append(h)
        else:
            dc2 = h.split("-")[-1]
            secondlist.append(h)
#    print firstlist, dc1
#    print secondlist, dc2


    content1 = '''### ''' + dc1.upper() + ''' ###''' + '\n\n'
    for i in firstlist:
        content1 = content1 + i + "\n"

    content2 = '\n' + '''### ''' + dc2.upper() + ''' ###''' + '\n\n'
    for j in secondlist:
        content2 = content2 + j + "\n"

    desc = content1 + content2

    return desc,pod,dc1,dc2

def lb_login_us(desc,pr,dr,pod):
    lb_login_desc = "Please add the following hosts in LB LOGIN VIP pool.\n\n" + desc
    lb_login_subj = "Subject: " + pr.upper() + " & " + dr.upper() + " LB LOGIN Pool Addition | " + pod.upper() + " App Server cap add "
    return lb_login_subj,lb_login_desc

def lb_us(desc,pr,dr,pod):
    lb_us_desc = "Please add the following hosts in LB VIP pool.\n\n" + desc
    lb_us_subj = "Subject: " + pr.upper() + " & " + dr.upper() + " LB VIP Pool Addition | " + pod.upper() + " App Server cap add "
    return lb_us_subj,lb_us_desc

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--ifile', help='input file contains list of hostnames to be verified')
    args=parser.parse_args()

    if len(sys.argv) < 3:
        parser.print_help()
        parser.exit(1)

    if args.ifile:
        ifile = args.ifile

    desc,pod,dc1,dc2=create_description(ifile)

    lb_login_subj,lb_login_desc = lb_login_us(desc,dc1,dc2,pod)
    print lb_login_subj
    print lb_login_desc

    lb_us_subj,lb_us_desc = lb_us(desc,dc1,dc2,pod)
    print lb_us_subj
    print lb_us_desc

if __name__ == '__main__':
    main()

