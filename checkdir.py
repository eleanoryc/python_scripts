
# script to check the existence of path, one segment at a time

import os

filename='Users/echeung/Documents/salesforce/python_script/pythonclass/x'
filetoadd=''


for path_segment in filename.split('/'):
    if filetoadd:
        filetoadd += '/'
    filetoadd += path_segment
    print filetoadd
    if not os.path.isdir('/'+filetoadd):
        print filetoadd + " not a dir"
        break


