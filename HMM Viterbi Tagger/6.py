#!/usr/bin/python3


import math

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# returns the probability of a word/label pair
def get_emission_count(emission_dict, labels_dict, word, label):
    numerator = 0
    denominator = 0

    if (word, label) in emission_dict:
        numerator = emission_dict[(word,label)]

    denominator = labels_dict[label]

    return numerator/denominator


if __name__ == "__main__":
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
    file2 = open("ner_train_new.dat", 'w')

    for line in file1:
        words = line.split(" ")
        if words[0] == "\n":
            file2.write(words[0])
        else:
            if worddict[words[0]] < 5:
                if is_number(words[0]):
                    file2.write('NUM ' + words[1])
                elif words[0].istitle():
                    file2.write('TITLE ' + words[1])
                elif words[0].isupper():
                    file2.write('UPPER ' + words[1])
                else:
                    file2.write('_RARE_ ' + words[1])
            else:
                file2.write(words[0] + ' ' + words[1])

    # close files
    file1.close()
    file2.close()


    emission_dict = {} # dictionary of number of instances of word/label combo
    word_dict = {} # dictionary of words
    labels_dict = {} # dictionary of labels: count of label in training set
    trigram_dict = {} # dictionary of trigrams ((x1,x2,x3): log prob) from 5_1.txt
    labels_list = [] # list of labels

    # Fill emission dict, word dict, and labels
    rare_wordcounts = open('ner_new.counts', 'r')
    for line in rare_wordcounts:
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
                labels_list.append(words[2])
    rare_wordcounts.close()

    # Fill trigram_dict
    trigram_file = open('5_1.txt', 'r')
    for line in trigram_file:
        words = line.strip("\n").split(" ")
        trigram_dict[(words[0], words[1], words[2])] = words[3]
    trigram_file.close()


    # begin viterbi
    testfile = open('ner_dev.dat', 'r')
    file_to_write = open('6.txt', 'w')
    sentence = []

    for line in testfile:
        word = line.strip("\n")
        sentence.append(word)

        if not word: # if it is a blank line, representing end of sentence
            # perform viterbi on the sentence
            sentence_length = len(sentence) - 1
            pi = {}
            bp = {}
            for k in range(1, sentence_length + 1): # For k = i..n
                pi[(0,'*','*')] = 1

                Sk_2 = ['*']
                Sk_1 = ['*']
                Sk = labels_list

                if k >= 2:
                    Sk_1 = labels_list
                if k >= 3:
                    Sk_2 = labels_list

                for u in Sk_1:
                    for v in Sk:
                        for w in Sk_2:
                            q_val = 0
                            e_val = 0

                            if sentence[k-1] in word_dict:
                                if(get_emission_count(emission_dict, labels_dict, sentence[k - 1], v) == 0):
                                    e_val = float('-inf')
                                else:
                                    e_val = math.log(get_emission_count(emission_dict, labels_dict, sentence[k - 1], v))
                            else:
                                if (get_emission_count(emission_dict, labels_dict, '_RARE_', v) == 0):
                                    e_val = float('-inf')
                                else:
                                    e_val = math.log(get_emission_count(emission_dict, labels_dict, '_RARE_', v))
                            if (w,u,v) not in trigram_dict:
                                q_val = float('-inf')
                            else:
                                q_val = float(trigram_dict[(w, u, v)])
                            curr_pi_val = pi[(k-1,w,u)] + q_val + e_val
                            if (k,u,v) not in pi:
                                pi[(k,u,v)] = curr_pi_val
                            if (k,u,v) not in bp:
                                bp[(k,u,v)] = w
                            if pi[(k,u,v)] < curr_pi_val:
                                pi[(k, u, v)] = curr_pi_val
                                bp[(k,u,v)] = w


            # find (yn-1 yn argmax u,v)
            pi_max = float('-inf')
            u_max_label = ''
            v_max_label = ''

            for u in labels_list:
                for v in labels_list:
                    if sentence_length == 1:
                        if pi[(sentence_length,'*',v)] > pi_max:
                            pi_max = pi[(sentence_length,'*',v)]
                            u_max_label = u
                            v_max_label = v
                    else:
                        if pi[(sentence_length,u,v)] > pi_max:
                            pi_max = pi[(sentence_length,u,v)]
                            u_max_label = u
                            v_max_label = v

            labels_tagged = [u_max_label, v_max_label]
            counter = sentence_length-2
            while counter > 0:
                yk = bp[(counter+2, labels_tagged[0], labels_tagged[1])]
                labels_tagged = [yk] + labels_tagged
                counter = counter - 1
            pi_values = []
            counter = sentence_length
            while counter > 0:
                new_pi = 0
                if counter == 1:
                    new_pi = pi[(counter, '*', labels_tagged[counter-1])]
                else:
                    new_pi = pi[(counter, labels_tagged[counter-2], labels_tagged[counter-1])]
                pi_values = [new_pi] + pi_values
                counter = counter - 1

            # write into new file
            while counter < sentence_length:
                file_to_write.write(sentence[counter] + ' ' + labels_tagged[counter] + ' ' + str(pi_values[counter]) + '\n')
                counter = counter + 1


            # write to new file 5_2 the current word, label, then pi probability

            file_to_write.write('\n')
            sentence = [] # then reset sentence to add new one

    testfile.close()
    file_to_write.close()



