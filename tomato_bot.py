#!/usr/bin/python
import praw
import re
import os
import pickle

if not os.path.isfile("tomato_config.txt"):
	print "You must create the file tomato_config.txt with the pickled credentials."
	exit(1)
else:
	print "Loading credentials..."
	user_data = pickle.load(open("tomato_config.txt", "rb"))
	#print user_data
