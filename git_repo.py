#!/usr/bin/python

git_repo_list = [ 'NCC_service_def_files', 'connectivity-checker', 'netutils', 'pod_ncc', 'estates', 'tools' ]

for git_repo in git_repo_list:

    if git_repo == 'estates':
        GIT_CLONE_CMD = 'git clone https://git.soma.salesforce.com/estates/'
        print GIT_CLONE_CMD + git_repo
    elif git_repo == 'tools':
        GIT_CLONE_CMD = 'git clone https://git.soma.salesforce.com/echeung/'
        print GIT_CLONE_CMD + git_repo
    else:
        GIT_CLONE_CMD = 'git clone https://git.soma.salesforce.com/imt/'
        print GIT_CLONE_CMD + git_repo
