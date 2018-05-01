
# create a script to parse log file

# apache log, which will consist of 7/8 fields
# first read file into a list, line by line

# check the number of occurances from the same source ips, which will be on field one, say


## read file, and print line by line
#with open ("myapp.log", "r") as rFileHandle:
#    for line in rFileHandle:
#        print line,

#print


## read file, and add each line to an array
#lines=''
#with open ("myapp.log", "r") as rFileHandle:
#    for line in rFileHandle:
#        lines+=line
#    print lines

#print


## read log file line by line
## assign user to 2nd field of the line
## assign status to 3rd field of the line
## count number of occurence of user

dict = {}
list = []
count = 0
with open ("myapp.log", "r") as rFileHandle:
    for line in rFileHandle:
         user = line.split(":")[1]
         status = line.split(":")[2]

#         print user,status

#         if not user in list:
#             list.append(user)
#             dict[user] = count + 1
#         else:
#             print user
#             dict[user] = count + 1

#    print dict


         if not user in dict:
             dict[user] = count + 1 
         else:
             dict[user] += 1 

    print dict
         

         # put it in dict, and do the count at the end


#print lines

#summaryData = line.split(",")[-1]

#            for path_segment in filename.split('/'):
