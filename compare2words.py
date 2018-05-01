
''' Write a function to return if two words are exactly "one edit" away, where an edit is:

    Inserting one character anywhere in the word (including at the beginning and end)
    Removing one character
    Replacing exactly one character
'''

def difference(word1,word2):
    nodiff = 0
    if len(word1) == len(word2):
        print("print same length")
        for i in range(len(word1)):
            if word1[i] != word2[i]:
                nodiff += 1
        print nodiff  

    elif (len(word1) - len(word2)) == -1:
        print("check if a character is added or not")
        for i in range(len(word1)):
            if word1[i] != word2[i]:
                nodiff += 1
        
        print nodiff

    elif (len(word1) - len(word2)) == 1:
        print("added if a character is removed or not")
            #for i in range(len(word1)):

    else:
        print("doesn't fit")



word1 = 'ABCD'
word2 = 'ZABCD'

#word1 = 'ABCD'
#word2 = 'ABCDE'

#word1 = 'ABCD'
#word2 = 'BCDEF'


difference(word1,word2)
print word1
print word2
