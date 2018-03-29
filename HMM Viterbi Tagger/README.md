Hidden Markov Model Tagger using the Viterbi Algorithm:
------------------------------------------------------

Takes sentences as input and determines the most likely part of speech tag sequence using a machine learning based language classifier. Project written in python 3.6.3, so it may be necessary to replace "python" in the commands with "python3"

------------------------------

4_1.py: Takes data from ner_train.dat and replaces infrequent words with a new class called "_RARE_", to improve future tagging. Creates ner_train_RARE.dat, a new version of ner_train.dat but with infrequent words replaced with "_RARE_"

4_2.py: Finds basic word-given-tag log probabilities for each word in the ner_train_RARE.dat training file and then assigns tags to test data from der_dev.dat file

5_1.py: Creates textfile with all of the seen trigram tags seen in training data (e.g. Noun, verb, noun) along with the log likelihood of that trigram

5_2.py: Tags words like in 4_2.py, but much more accurately using the Viterbi Algorithm

-----------------------------

To see results of this project, execute the following commands (in order listed):

python 4_1.py

python 4_2.py

python eval_ne_tagger.py ner_dev.key 4_2.txt
      
   Will print out the results of a basic tagger on the test dataset
      
python 5_1.py

python 5_2.py

python eval_ne_tagger.py ner_dev.key 5_2.txt
      
   Will print out the improved results on the test dataset with the viterbi tagger


