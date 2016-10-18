import argparse

url = "https://imt.dmz.salesforce.com/api/v1/observers/reports/?provider="

def main(argv=None):

    url = "https://imt.dmz.salesforce.com/api/v1/observers/reports/?provider="
    parser = argparse.ArgumentParser()
    parser.add_argument('--rtype', help="Config Checker or Prodtest")
    parser.add_argument('--pod', help='Specify an instance')
    #args = ArgParser.parse_args(args=argv)
    args=parser.parse_args()

    if args.rtype:
        rtype = args.rtype
        if ( rtype != 'configchecker' ) and ( rtype != 'prodtest' ):
        #if rtype != 'configchecker':
            print 'error'
            exit(1)
        if rtype == 'configchecker':
             url += 'config-checker'
             print url
        if rtype == 'prodtest':
             url += 'smoke-test'
             print url

    if args.pod:
        pod = args.pod
        print pod

        url += '&instance='+pod
    print url

    exit(0) 

if __name__ == '__main__':
    main()
