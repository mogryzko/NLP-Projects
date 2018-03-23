#!/usr/bin/python3

import math

# returns the probability of a word/label pair
def get_emission_count(emission_dict, labels_dict, word, label):
    numerator = 0
    denominator = 0

    if (word, label) in emission_dict:
        numerator = emission_dict[(word,label)]
    denominator = labels_dict[label]

    return numerator/denominator

def tagger(emission_dict, labels_dict, word):
    prediction = 0
    label = ''
    for key in labels_dict:
        curr_emission = get_emission_count(emission_dict, labels_dict, word, key)
        if prediction < curr_emission:
            prediction = curr_emission
            label = key


    return (label, prediction)

if __name__ == "__main__":

    file = open("ner_rare.counts", 'r')

    # build dictionary of word counts
    emission_dict = {}
    word_dict = {}
    labels_dict = {}
    for line in file:
        words = line.strip("\n").split(" ")
        if words[1] == 'WORDTAG':
            emission_dict[(words[3], words[2])] = int(words[0])
            if words[3] in word_dict:
                word_dict[words[3]] += int(words[0])
            else:
                word_dict[words[3]] = int(words[0])
            if words[2] in labels_dict:
                labels_dict[words[2]] += int(words[0])
            else:
                labels_dict[words[2]] = int(words[0])

    file.close()

    # create new file "4_2.txt" with argmax log emission estimates
    newfile = open("4_2.txt", 'w')

    # open ner_dev.dat file to read in words for predictions
    file = open("ner_dev.dat", 'r')

    for line in file:
        word = line.strip("\n")
        if word:
            if word in word_dict:
                prediction = tagger(emission_dict, labels_dict, word)
                newfile.write(word + ' ' + prediction[0] + ' ' + str(math.log(prediction[1])) + '\n')
            else:
                prediction = tagger(emission_dict, labels_dict, '_RARE_')
                newfile.write(word + ' ' + prediction[0] + ' ' + str(math.log(prediction[1])) + '\n')
        else:
            newfile.write('\n')
    file.close()
    newfile.close()









