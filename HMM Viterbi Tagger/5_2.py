#!/usr/bin/python3

import math

emission_dict = {}  # dictionary of number of instances of word/label combo
word_dict = {}  # dictionary of words and number of times they appear in training data
labels_dict = {}  # dictionary of labels: count of label in training set
trigram_dict = {}  # dictionary of trigrams ((x1,x2,x3): log prob) from 5_1.txt
labels_list = []  # list of labels



# returns the probability of a word/label pair
def get_emission_count(emission_dict, labels_dict, word, label):
    numerator = 0
    denominator = 0
    if (word, label) in emission_dict:
        numerator = emission_dict[(word, label)]
    denominator = labels_dict[label]

    return numerator / denominator

# fills all dictionaries with training data, to be used later by viterbi algorithm
def fillDicts(rare_wordcounts, trigram_file):
    for line in rare_wordcounts:
        words = line.strip("\n").split(" ")
        if words[1] == 'WORDTAG':
            emission_dict[(words[3], words[2])] = int(words[0])
            # fill word_dict
            word_dict.setdefault(words[3],0)
            word_dict[words[3]] += int(words[0])
            # fill labels_dict, append to labels_list if we haven't seen the label before
            if (labels_dict.setdefault(words[2],0) == 0):
                labels_list.append(words[2])
            labels_dict[words[2]] += int(words[0])
    # fill trigram_dict
    for line in trigram_file:
        words = line.strip("\n").split(" ")
        trigram_dict[words[0], words[1], words[2]] = words[3]

# takes in a sentence, performs viterbi algorithm on it and returns max likelihood tags and probabilities
def viterbi(sentence):
    sentence_length = len(sentence) - 1
    for k in range(1, sentence_length + 1):
        pi[(0, '*', '*')] = 1  # base case for algorithm
        Sk_2 = ['*']  # list of potential labels for word i-2
        Sk_1 = ['*']  # list of potential labels for word i-1
        Sk = labels_list  # list of potential labels for word i
        if k >= 2:
            Sk_1 = labels_list  # Once * base case has been hit
        if k >= 3:
            Sk_2 = labels_list  # Once *,* base cases have been hit
        for u in Sk_1:
            for v in Sk:
                for w in Sk_2:
                    q_val = 0
                    e_val = 0
                    if sentence[k - 1] in word_dict:
                        temp = get_emission_count(emission_dict, labels_dict, sentence[k - 1], v)
                    else:
                        temp = get_emission_count(emission_dict, labels_dict, '_RARE_', v)
                    if (temp == 0):
                        e_val = float('-inf')
                    else:
                        e_val = math.log(temp)
                    q_val = float(trigram_dict.setdefault((w, u, v), float('-inf')))
                    curr_pi_val = pi[(k - 1, w, u)] + q_val + e_val
                    pi.setdefault((k, u, v), curr_pi_val)
                    bp.setdefault((k, u, v), w)
                    # update pi and bp dictionaries so they contain argmax values
                    if pi[(k, u, v)] < curr_pi_val:
                        pi[(k, u, v)] = curr_pi_val
                        bp[(k, u, v)] = w
    # find most likely tags (u,v) for end of sentence
    pi_max = float('-inf')
    u_max_label = ''
    v_max_label = ''
    for u in labels_list:
        for v in labels_list:
            if sentence_length == 1:
                pi_val = pi[(sentence_length, '*', v)]
            else:
                pi_val = pi[(sentence_length, u, v)]
            if pi_val > pi_max:
                pi_max = pi_val
                u_max_label = u
                v_max_label = v

    # Backtrack and find most likely tags for rest of sentence
    labels_tagged = [u_max_label, v_max_label]
    counter = sentence_length - 2
    while counter > 0:
        yk = bp[(counter + 2, labels_tagged[0], labels_tagged[1])]
        labels_tagged = [yk] + labels_tagged
        counter = counter - 1
    # Backtrack and find log probabilities for those tags
    pi_values = []
    counter = sentence_length
    while counter > 0:
        if counter == 1:
            new_pi = pi[(counter, '*', labels_tagged[counter - 1])]
        else:
            new_pi = pi[(counter, labels_tagged[counter - 2], labels_tagged[counter - 1])]
        pi_values = [new_pi] + pi_values
        counter = counter - 1
    return labels_tagged,pi_values


if __name__ == "__main__":

    # open files with training data
    rare_wordcounts = open('ner_rare.counts', 'r')
    trigram_file = open('5_1.txt', 'r')

    # fill emission dict, word dict, trigram_dict, and labels_list
    fillDicts(rare_wordcounts, trigram_file)

    # close files with training data
    trigram_file.close()
    rare_wordcounts.close()

    # now use training data to perform viterbi algorithm on test data
    testfile = open('ner_dev.dat', 'r')
    file_to_write = open('5_2.txt', 'w')
    sentence = []
    for line in testfile:
        word = line.strip("\n")
        sentence.append(word)
        pi = {}  # maximum likelihood probabilities for each tag
        bp = {}  # argmax for each word
        if not word:  # if it is a blank line, representing end of sentence
            labels_tagged,pi_values = viterbi(sentence) # send sentence to viterbi
            # then write into new file
            for i in range(0, len(sentence)-1):
                file_to_write.write(sentence[i] + ' ' + labels_tagged[i] + ' ' + str(pi_values[i]) + '\n')
            file_to_write.write('\n')
            sentence = []  # then reset sentence to perform viterbi on next one in test set

    # finally, close files
    testfile.close()
    file_to_write.close()
