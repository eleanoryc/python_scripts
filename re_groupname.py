
import re
match = re.search('(?P<name>.*) (?P<phone>.*)', 'John 123456')

name = match.group('name')
phone = match.group('phone')

print name
print phone
