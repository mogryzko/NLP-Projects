#!/usr/local/bin/python2.7

import os, sys

if __name__ == "__main__":
    if sys.argv[1] == 'q4':
        os.system("python2.7 count_cfg_freq.py " + sys.argv[2] + "> cfg.counts")
        os.system("python2.7 q4.py " + sys.argv[2] + " " + sys.argv[3])
    if sys.argv[1] == 'q5':
        os.system("python2.7 count_cfg_freq.py " + sys.argv[2] + "> cfg.counts")
        os.system("python2.7 q5.py " + sys.argv[2] + " " + sys.argv[3] + " " + sys.argv[4])
    if sys.argv[1] == 'q6':
        os.system("python2.7 count_cfg_freq.py " + sys.argv[2] + "> cfg.counts")
        os.system("python2.7 q6.py " + sys.argv[2] + " " + sys.argv[3] + " " + sys.argv[4])