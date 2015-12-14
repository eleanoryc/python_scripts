import re

list = [ 'abc', 'dff', 'iob', 'man', 'pop' ]
found = 0

print list

pattern='b'
for x in list:
    if re.search(pattern,x):
        print "found " + pattern + " in: " + x
        found=found+1

print "Number of occurences for " + pattern + " : " + str(found)

