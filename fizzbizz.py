for num in range(1,31):
    if num % 3 == 0 and num % 5 == 0:
        print "facebook"
    elif num % 3 == 0:
        print "face"
        continue
    elif num % 5 == 0:
        print "book"
    else:
        print num


word = []
for i in xrange(1,n+1):
    if i % 3 == 0 and i % 5 == 0:
        word.append("FizzBuzz")
    elif i % 3 == 0:
        word.append("Fizz")
    elif i % 5 == 0:
        word.append("Buzz")
    else:
        word.append(str(i))
    return word
