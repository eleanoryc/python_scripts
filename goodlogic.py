

def generateAclDatasets(aclData, srcList, dstList, proto, portList, lineNum, multi_flag):
    # a list with non-sshable domains
    non_sshable_domains = [ 'data.sfdc.net' ]
    for port in portList:
        for srcHost in srcList:
            # Get the site name from the src list
            s_site = extractSiteNameFromHost(srcHost)
            for dstHost in dstList:
                d_site = extractSiteNameFromHost(dstHost)
                if s_site == d_site:

##### ***** set non_sshable to False first, then loop through domains, if requirement met, set non_sshable to True, and break  #########

                    non_sshable = False
                    for domain in non_sshable_domains:
                        if re.search(domain, dstHost):
                             non_sshable = True
                             break
                    if non_sshable:
                        dataset_tuple = (srcHost, dstHost, port, '--no-check-listener')
                    else:
                        dataset_tuple = (srcHost, dstHost, port)
                    #if multi_flag is not set, then no need to track the line numbers
                    if multi_flag:
                        key = s_site + "_intrasite_" + str(lineNum)
                    else:
                        key = s_site + "_intrasite"
                else:
                    dataset_tuple = (srcHost, dstHost, port)
                    #if multi_flag is not set, then no need to track the line numbers
                    if multi_flag:
                        key = s_site + "_intersite_" + str(lineNum)
                    else:
                        key = s_site + "_intersite"
                aclData[key].append(dataset_tuple)

    for key in aclData.keys():
        logger.debug("DATA SET : " + key)
