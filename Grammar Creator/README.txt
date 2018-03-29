Grammar Tree Tagger using Cocke–Younger–Kasami (CYK) algorithm
---------------------------------------------------------

Learns from dataset of grammar trees (parse_train.dat) and finds most likely grammar tree tag sequence for test data (parse_dev.dat). All files for this project are written in python 2.7

----------------------------------

4.py: finds rare words in training data and replaces them with RARE. Output file: parse_train.RARE.dat
5.py: First implimentation of CYK algorithm. 
      Prediction file outputted: q5_prediction_file 
      Results: q5_eval.txt
6.py: Improved implimentation of CYK algorithm with use of vertical markovization techniques. 
      Prediction file outputted: q6_prediction_file 
      Results: q6_eval.txt
parser.py: Python script that specifies python version 2.7

---------------------------------

Files should be run as such:

First run this to create new file with RARE counts:
      ./parser.py q4 parse_train.dat parse_train.RARE.dat

Grammar:
      ./parser.py q5 parse_train.RARE.dat parse_dev.dat q5_prediction_file
      python2.7 eval_parser.py parse_dev.key q5_prediction_file > q5_eval.txt
            - q5_eval.txt will contain results
            - Runtime 70 seconds

With Vertical Markovization:
      ./parser.py q4 parse_train_vert.dat parse_train_vert.RARE.dat
      ./parser.py q6 parse_train_vert.RARE.dat parse_dev.dat q6_prediction_file
      python2.7 eval_parser.py parse_dev.key q6_prediction_file > q6_eval.txt
            - q6_eval.txt will contain results
            - Runtime 128 seconds




