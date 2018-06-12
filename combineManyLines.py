import re
with open ("manylines", "r") as rFileHandle:
    newline = ''
    for line in rFileHandle:
       regexline = re.compile("\"$")
       # if not finding line ending with ' " ', then combine the line
       if not regexline.search(line):
             newline = newline + line.strip() + " "
             continue
       # if finding line ending with ' " ', then remove newline character, and the ' " ', and print newline
       else:
             newline = newline + line.strip()[:-1]
             print newline
             newline = ''

