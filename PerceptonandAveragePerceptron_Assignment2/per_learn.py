import os
import sys
import random
#from functools import lru_cache

weight = 0
vocabulary = {}
bias = 0
maxiterations=20
email = []
ham = set()
spam = set()


if len(sys.argv) != 2:
    print("Missing the location of the training data")
else:
    rootFolder = sys.argv[1]
fileModel="per_model.txt"
encodinglatin="latin1"

import datetime
print(datetime.datetime.now())

for root, subFolders, files in os.walk(rootFolder):
    filename=root.split("/")[-1].lower()
    if filename == 'ham':
        for name in files:
            file = open(os.path.join(root, name), 'r', encoding=encodinglatin)
            emaildata = file.read()
            email.append(emaildata)
            ham.add(emaildata)
        file.close()
    elif filename == 'spam':
        for name in files:
            file = open(os.path.join(root, name), 'r', encoding=encodinglatin)
            emaildata = file.read()
            email.append(emaildata)
            spam.add(emaildata)
        file.close()
for mail in email:
    words = mail.split()
    for word in words:
        if word not in vocabulary:
            vocabulary[word] = 0
for iteration in range(0, maxiterations):
    random.shuffle(email)
    for mail in email:
        weight = 0
        words = mail.split()
        for word in words:
            weight = weight + vocabulary[word]
        if mail in spam:
            label = 1
        else:
            label = -1
        activation = weight + bias
        if activation * label <=0:
            for word in words:
                vocabulary[word] = vocabulary[word] + label
            bias = bias + label

with open(fileModel, 'w', encoding=encodinglatin) as f:
    f.write(str(bias) + '\n')
    for key, value in vocabulary.items():
        f.write(str(key) + " " + str(value) + '\n')
print(datetime.datetime.now())
