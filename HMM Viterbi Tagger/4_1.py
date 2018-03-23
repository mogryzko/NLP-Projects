#!/usr/bin/python3

file1 = open("ner_train.dat", 'r')

# build dictionary of word counts
worddict = {}
for line in file1:
    words = line.strip("\n").split(" ")
    if not(words[0] == ''):
        if words[0] in worddict:
            worddict[words[0]] += 1
        else:
            worddict[words[0]] = 1

file1.close()
file1 = open("ner_train.dat", 'r')


# create "ner_train_rare.dat" file and replace infrequent words with "_RARE_"
file2 = open("ner_train_rare.dat", 'w')

for line in file1:
    words = line.split(" ")
    if words[0] == "\n":
        file2.write(words[0])
    else:
        if worddict[words[0]] < 5:
            file2.write('_RARE_ ' + words[1])
        else:
            file2.write(words[0] + ' ' + words[1])

# close files
file1.close()
file2.close()
