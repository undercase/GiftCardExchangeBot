import praw
import datetime
import time
import Queue

reddit = praw.Reddit("GiftCardExchange Warner v1.0 by /u/superman3275",)

reddit.login()

already_done = []
queue = Queue.Queue()

def comment(submission, commment):
	global queue
	global already_done
	try:
		submission.add_comment(comment)
		already_done.append(submission)
		print "Commented on submission " + vars(submission)["name"]
	except RateLimitExceeded:
		queue.put((submission, comment))

while True:

	subreddit = reddit.get_subreddit("giftcardexchange")

	for submission in subreddit.get_new(limit=10):

		while not queue.empty():
			item = queue.get()
			comment(item[0], item[1])

		if not (submission in already_done):
			author = vars(submission)["author"]
			comment_text = ""

			# Get account age
			author_created = datetime.datetime.fromtimestamp(int(author.created_utc))
			now = datetime.datetime.now()
			delta = now - author_created

			# Check account age
			if delta.days < 7:
				comment_text +=  "WARNING: This poster's account is less than a week old! Trade with caution!\n\n\n"
			elif delta.days < 31:
				comment_text += "WARNING: This poster's account is less than a month old! Trade with caution!\n\n\n"
			elif delta.days < 93:
				comment_text += "WARNING: This poster's account is less than three months old! Trade with caution!\n\n\n"
			else:
				comment_text += "This poster's account is older than three months! It fulfills the age requirement!!\n\n\n"

			# Check comment karma
			if author.comment_karma < 10:
				comment_text += "WARNING: This poster has very, very little (less than 10) karma! Trade with caution!\n\n\n"
			elif author.comment_karma < 100:
				comment_text += "WARNING: This poster has little (less than 100) karma! Trade with caution!\n\n\n"
			elif author.comment_karma < 300:
				comment_text += "WARNING: This poster has less-than-average (less than 300) karma! Trade with caution!\n\n\n"
			else:
				comment_text += "This poster has more than 300 karma! (S)he fulfills the karma requirement!\n\n\n"

			# Overall
			count = comment_text.count("WARNING")
			if count == 2:
				comment_text += "OVERALL: Do not trade with this poster! They do not fulfill any of this subreddit's requirements!!"
			elif count == 1:
				comment_text += "OVERALL: Be careful with this poster! They only fulfill one of this subreddit's requirements!"
			elif count == 0:
				comment_text += "OVERALL: This poster's account looks great! (Still be careful though)"
			
			comment(submission, comment_text)
	time.sleep(30)