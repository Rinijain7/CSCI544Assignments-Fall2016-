import os
import sys
import random
import datetime
from collections import defaultdict
from collections import Counter

if len(sys.argv) != 2:
    print("Missing the location of the training data")
else:
    rootFolder = sys.argv[1]
vocabulary=defaultdict(int)
email=defaultdict()
average_weight=defaultdict(int)
bias = 0
maxiterations=30
beta = 0
count = 1
ham = set()
spam = set()
fileModel="per_model.txt"
encodinglatin="latin1"
print(datetime.datetime.now())#checking the start time
for root, subFolders, files in os.walk(rootFolder):
    for name in files:
        anotherdict = defaultdict(int)
        path = os.path.join(root, name)
        with open(path, 'r', encoding=encodinglatin) as filename:
            data=filename.read()
            emaildata=data.split()
            if 'ham' in path:#checking the label of each file
                label=-1
            else:
                label=1
            for word in emaildata:
                if word in vocabulary:
                    continue
                else:
                    vocabulary[word]=0#creating vocabulary of each word
                    average_weight[word]=0#to calculate the average weight of each word
                email[path]={}
                email[path]['label']=label
                email[path]['anotherdict']=Counter(emaildata)#calculating the count of occurence of each feature
for iteration in range(0, maxiterations):#iterating for 30 times
    random.shuffle(list(email.keys()))#shuffling the files
    for mail in list(email.keys()):
        weight = 0
        anotherdict=email[mail]['anotherdict']
        label=email[mail]['label']
        weight=sum(vocabulary[word]*anotherdict[word] for word in anotherdict)#weight of the word
        activation=weight+bias#alpha value
        if (activation * label) <=0:
            for word in anotherdict:
                vocabulary[word]=vocabulary[word]+(label*anotherdict[word])
                average_weight[word]=average_weight[word]+(label*count*anotherdict[word])
            bias = bias + label
            beta = beta + (label * count)
        count = count + 1

# count=float(count)
for key,value in average_weight.items():
    average_weight[key]=vocabulary[key]-((1/count)*average_weight[key])

beta = bias - ((1/count)*beta)

with open(fileModel, 'w', encoding=encodinglatin) as f:
    f.write(str(bias) + '\n')
    for key, value in vocabulary.items():
        f.write(str(key) + " " + str(value) + '\n')

print(datetime.datetime.now())#checking the ending time
