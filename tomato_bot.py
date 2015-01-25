#!/usr/bin/python

# Tomato Bot created by /u/duffbuster
# Thanks to /u/fourthofabushel for the framework and starting point

import praw
import re
import os
import pickle
from rottentomatoes import RT

# rottentomatoes test
#res = RT().search('Toy Story 3')
#print res
#exit(1)
if not os.path.isfile("tomato_config.txt"):
	print "You must create the file tomato_config.txt with the pickled credentials."
	exit(1)
else:
	print "Loading credentials..."
	user_data = pickle.load(open("tomato_config.txt", "rb"))
	#print user_data

user_agent = ("Tomato bot 0.1 created by /u/duffbuster.")
r = praw.Reddit(user_agent = user_agent)

r.login(user_data[0], user_data[1])
del user_data

print "Logged in"

# Check replies
if not os.path.isfile("replies.txt"):
	replies = []
else:
	print "Loading previousl reply ids"
	with open("replies.txt", "r") as f:
		replies = f.read()
		replies = replies.split("\n")
		replies = filter(None, replies)

# Check for new stuff to reply to
# Just want to search comments here, don't care about posts 
subreddit = r.get_subreddit('umw_cpsc470z')
print "Checking for new posts"
for submission in subreddit.get_hot(limit=10):
	print "Checking comments"
	flat_comments = praw.helpers.flatten_tree(submission.comments)
	for comment in flat_comments:
		if comment.id not in replies:
			print comment.body
			if re.search("tomatometer: ", comment.body, re.IGNORECASE):
				# get movie from comment
				movie = re.search("tomatometer\: (.*)", comment.body, re.IGNORECASE).groups()
				print movie

				# make api call

				# spit out result
				print "Bot replying to comment: ", comment.id
				#comment.reply(REPLY)
				#replies.append(comment.id)

# Save new replies
print "Saving reply ids to file"
with open("replies.txt", "w") as f:
	for i in replies:
		f.write(i + "\n")	
