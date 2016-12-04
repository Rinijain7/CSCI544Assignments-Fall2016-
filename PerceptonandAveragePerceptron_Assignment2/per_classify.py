import os
import sys
output = []
countspam = 0
countham = 0
count_of_spam=0
count_of_ham=0
count_of_ham_prec=0
count_of_spam_prec=0
vocabulary = {}
fileModel="per_model.txt"
encodinglatin="latin1"

rootFolder = sys.argv[1]
outputfile = sys.argv[2]

with open(fileModel, 'r', encoding=encodinglatin) as f:
    bias = int(f.readline())
    lines = f.readlines()
    for line in lines:
        data = line.split()
        vocabulary[data[0]] = int(data[1])
path_of_file = []
email = []
for root, subFolders, files in os.walk(rootFolder):
    for fileName in files:
        filename=fileName.split(".")[-1]
        if filename == "txt":
            if 'spam' in fileName:
                count_of_spam=count_of_spam+1
            elif 'ham' in fileName:
                count_of_ham=count_of_ham+1
            f = open(os.path.join(root, fileName), 'r', encoding=encodinglatin)
            path_of_file.append(os.path.join(root, fileName))
            emaildata = f.read()
            email.append(emaildata)
for mail in email:
    words = mail.split()
    weight = 0
    for word in words:
        if word in vocabulary:
            weight = weight + vocabulary[word]
    final_weight = weight + vocabulary['bias']
    if final_weight< 0:
        if 'ham.txt' in fileName:
            count_of_ham_prec=count_of_ham_prec+1
        # else:
        #     count_of_spam_prec = count_of_spam_prec + 1
        countham = countham + 1
        output.append("ham")
    else:
        if 'spam.txt' in fileName:
            count_of_spam_prec = count_of_spam_prec + 1
        # else:
        #     count_of_ham_prec = count_of_ham_prec + 1
        countspam = countspam + 1
        output.append("spam")
per_output= open(outputfile, 'w',encoding=encodinglatin)
for i in range(len(output)):
    per_output.write(output[i] + " " + path_of_file[i] + "\n")

# precisionspam=round(countspam/count_of_spam_prec,2)
# print(precisionspam)
# precisionham=round(countham/count_of_ham_prec,2)
# print(precisionham)
#
# recallspam=round(countspam/count_of_spam,2)
# print(recallspam)
# recallham=round(countham/count_of_ham,1)
# print(recallham)
#
# f1spam=round((2*precisionspam*recallspam)/(precisionspam+recallspam),2)
# print(f1spam)
# f1ham=round((2*precisionham*recallham)/(precisionham+recallham),2)
# weightedaccuracy=(f1spam+f1ham)/2
# print(weightedaccuracy)
#
#print(precisionspam)
#print(precisionham)
#print(recallspam)
#print(recallham)
#print(f1spam)
#print(f1ham)
