Grammar Tagger using Cocke–Younger–Kasami (CYK) algorithm

Learns from dataset of grammars (parse_train.dat) and finds most likely grammar tag sequence for test data (parse_dev.dat).

4.py: finds rare words in training data and replaces them with RARE. Output file: parse_train.RARE.dat
5.py: First implimentation of CYK algorithm. Prediction file outputted: q5_prediction_file. Results: q5_eval.txt
6.py: Improved implimentation of CYK algorithm, with faster speed and use of vertical markovization techniques.
      Prediciton file outputted: 
