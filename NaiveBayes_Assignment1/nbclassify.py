import sys
import os
countpspam=0
countpham=0
spam_prior = 0
ham_prior = 0
count_of_spam=0
count_of_ham=0
spam_dict = {}
ham_dict = {}
count_of_spam_prec=0
count_of_ham_prec=0
with open('nbmodel.txt') as file:
    lines = file.readlines()

    spam_prior = float(lines[0].strip())
    ham_prior = float(lines[1].strip())

    for line in lines[2:]:
        lineContent = line.split('::')

        word = lineContent[0]
        NBclass = lineContent[1]
        prob = float(lineContent[2])

        if NBclass == 'spam':
            spam_dict[word] = prob
        else:
            ham_dict[word] = prob

def classifymail(fileLocation):
    global count_of_spam, count_of_ham, count_of_spam_prec,count_of_ham_prec
    global spam_dict, ham_dict, spam_prior, ham_prior
    global countpspam,countpham
    spam_prob = spam_prior
    ham_prob = ham_prior

    with open(fileLocation,"r", encoding="latin1") as testData:
        mail = testData.read().split()
        if 'spam' in fileLocation:
            count_of_spam = count_of_spam + 1
        else:
            count_of_ham = count_of_ham + 1
        for word in mail:
            if word in spam_dict:
                spam_prob += spam_dict[word]
                ham_prob += ham_dict[word]
        if spam_prob>ham_prob and 'spam' in fileLocation:
            count_of_spam_prec=count_of_spam_prec+1
        elif ham_prob>spam_prob and 'ham' in fileLocation:
            count_of_ham_prec=count_of_ham_prec+1

        if spam_prob > ham_prob:
            countpspam=countpspam+1
            return 'spam ' + fileLocation
        else:
            countpham=countpham+1
            return 'ham ' + fileLocation


def getAllwords(rootFolder):

    mails = []
    for root, dirs, files in os.walk(rootFolder, topdown=False):
        for name in files:
            if name.endswith(".txt"):
                mails.append(os.path.join(root, name))
    return mails
if len(sys.argv) != 2:
    print("Missing the location of the test data")
else:
    rootFolder = sys.argv[1]
    mails = getAllwords(rootFolder)

    output = open('nboutput.txt', 'w')
    for mail in mails:
        output.write(classifymail(mail) + '\n')


precisionspam=round(countpspam/count_of_spam_prec,2)
precisionham=round(countpham/count_of_ham_prec,2)

recallspam=round(countpspam/count_of_spam,2)
recallham=round(countpham/count_of_ham,2)

f1spam=round((2*precisionspam*recallspam)/(precisionspam+recallspam),2)
f1ham=round((2*precisionham*recallham)/(precisionham+recallham),2)

#print(precisionspam)
#print(precisionham)
#print(recallspam)
#print(recallham)
#print(f1spam)
#print(f1ham)