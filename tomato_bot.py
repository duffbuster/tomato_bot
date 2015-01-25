#!/usr/bin/python

# Tomato Bot created by /u/duffbuster
# Thanks to /u/fourthofabushel for the framework and starting point

import praw
import re
import os
import pickle
from rottentomatoes import RT

REPLY = ""
rt = RT()

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
	print "Loading previous reply ids"
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
			if re.search("tomatometer: ", comment.body, re.IGNORECASE):
				# get movie from comment
				movie = re.search("tomatometer\: (.*)", comment.body, re.IGNORECASE).groups()

				# make api call
				res = rt.search(movie[0], page_limit=1)
				if not res:
					REPLY = "No results found."
				else:
					ratings = res[0]["ratings"]
					year = res[0]["year"]
				
					# spit out result
					print "Bot replying to comment: ", comment.id
					REPLY = movie[0]+'\n\n'+'====================\n\n'+'Year: '+str(year)+'\n\n'+'Audience Rating: '+str(ratings["audience_rating"])+'\n\n'+'Audience Score: '+str(ratings["audience_score"])+'\n\n'+'Critics Rating: '+str(ratings["critics_rating"])+'\n\n'+'Critics Score: '+str(ratings["critics_score"])+'\n\n'

				comment.reply(REPLY)
				replies.append(comment.id)

# Save new replies
print "Saving reply ids to file"
with open("replies.txt", "w") as f:
	for i in replies:
		f.write(i + "\n")	
