import sys
import os
import math

spam_file_count = 0
ham_file_count = 0

spam_dict = {}
ham_dict = {}
unique_words = set()

def getClass(fileLocation):
    if 'spam' in fileLocation.split('/')[-2]:
        return 'spam'
    elif 'ham' in fileLocation.split('/')[-2]:
        return 'ham'

def wordCount(dict):
    total_count = 0
    for word, count in dict.items():
        total_count += count

    return total_count

def getAllwords(rootFolder):
    mails = []
    for root, dirs, files in os.walk(rootFolder, topdown=False):
        for name in files:
            if name.endswith(".txt"):
                mails.append(os.path.join(root, name))
    return mails

def learn(fileLocation):
    global spam_file_count, ham_file_count

    fileObj = open(fileLocation,"r", encoding="latin1")

    NBclass = getClass(fileLocation)

    if NBclass == 'spam':
        spam_file_count += 1
    else:
        ham_file_count += 1

    mail = fileObj.read().split()
    for mailWord in mail:
        unique_words.add(mailWord)
        if NBclass == 'spam':
            if mailWord in spam_dict:
                spam_dict[mailWord] += 1
            else:
                spam_dict[mailWord] = 1
        else:
            if mailWord in ham_dict:
                ham_dict[mailWord] += 1
            else:
                ham_dict[mailWord] = 1

if len(sys.argv) != 2:
    print("Missing the location of the training data")
else:
    rootFolder = sys.argv[1]
    data = list(scan_data(train_dir))
    mails = getAllwords(rootFolder)
    for mail in mails:
        learn(mail)

for word in unique_words:
    if word not in spam_dict:
        spam_dict[word] = 0
    if word not in ham_dict:
        ham_dict[word] = 0

for word, count in spam_dict.items():
    spam_dict[word] += 1

for word, count in ham_dict.items():
    ham_dict[word] += 1

spam_count = wordCount(spam_dict)
ham_count = wordCount(ham_dict)

output = open('nbmodel.txt', "w")

spam_prior = spam_file_count / (spam_file_count + ham_file_count)
ham_prior = ham_file_count / (spam_file_count + ham_file_count)
output.write(str(spam_prior) + '\n')
output.write(str(ham_prior) + '\n')

for word, count in spam_dict.items():
    output.write(word + '::' + 'spam' + '::' + str(math.log(count/spam_count)) + '\n')

for word, count in ham_dict.items():
    output.write(word + '::' + 'ham' + '::' + str(math.log(count / ham_count)) + '\n')


