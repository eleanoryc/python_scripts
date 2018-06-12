

#keyList = {}
list = [ 'Name': 'Zara', 'Age': 7, 'Class': 'First' ]
dict = {}

keyTokens = list.split(",")
for tokens in keyTokens:
    keyPairs = tokens.split(":")
    print keyPairs


#if args.keyword_substitution:
#    keywords = args.keyword_substitution
#    keyTokens = keywords.split(",")
#    for tokens in keyTokens:
#        keyPairs = tokens.split(":")
#        if len(keyPairs) != 2:
#            print("Syntax error in specifying -keyword_substitution argument.\nSyntax: -keyword_substitution '<KEY>:<VALUE>,<KEY>:<VALUE>,<KEY>:<VALUE>'")
#            exit(1)
#        keyList[keyPairs[0].strip()] = keyPairs[1].strip()

