import re
list = ["Protein XVZ [Human]","Protein ABC [Mouse]","go UDP[3] glucosamine N-acyltransferase [virus1]","Protein CDY [Chicken [type1]]","Protein BBC [type 2] [Bacteria] [cat] [mat]","gi p19-gag protein [2] [Human T-lymphotropic virus 2]"]
pattern = re.compile("\[(.*?)\]$")
for string in list:
    match = re.search(pattern,string)
    lastBracket = re.split("\].*\[",match.group(1))[-1]
    print lastBracket
