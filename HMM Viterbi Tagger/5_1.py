#!/usr/bin/python3


import math


def trigram_prob(labels):
    file = open('ner_rare.counts', 'r')

    numerator = 0
    denominator = 0

    for line in file:
        words = line.strip("\n").split(" ")
        if words[1] == '3-GRAM':
            if (words[2] == labels[0]) and (words[3] == labels[1]) and (words[4] == labels[2]):
                numerator = int(words[0])
        if words[1] == '2-GRAM':
            if (words[2] == labels[0]) and (words[3] == labels[1]):
                denominator = int(words[0])

    file.close()
    return numerator/denominator


if __name__ == "__main__":

    file = open('trigrams.txt', 'r')
    newfile = open('5_1.txt', 'w')

    for line in file:
        words = line.strip("\n").split(" ")
        newfile.write(words[0] + ' ' + words[1] + ' ' + words[2] + ' ')
        prob = trigram_prob((words[0], words[1], words[2]))
        log_prob = math.log(prob)
        newfile.write(str(log_prob) + '\n')

    file.close()
    newfile.close()