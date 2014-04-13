import praw
import datetime
import time
import Queue

reddit = praw.Reddit("GiftCardExchange Warner v1.0 by /u/superman3275",)

reddit.login()

already_done = []
queue = Queue.Queue()

# Generate scammers list
with open("scammers.txt", "r") as scammer:
	scammers = scammer.readlines()
for scammer in range(len(scammers)):
	scammers[scammer] = scammers[scammer].strip()
with open("confirmed.txt", "r") as confirm:
	confirmed = confirm.readlines()
for confirm in range(len(confirmed)):
	confirmed[confirm] = confirmed[confirm].strip()

def comment(submission, comment_text):
	global queue
	global already_done
	comment_text += "\n\n\n[Donate to the Creator of this Bot (Please)!](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=A3HSK4BPG56BU)"
	try:
		if vars(submission)["name"] not in already_done:
			submission.add_comment(comment_text)
			already_done.append(vars(submission)["name"])
			print "Commented on submission " + vars(submission)["name"]
	except praw.errors.RateLimitExceeded:
		queue.put((submission, comment_text))

while True:

	subreddit = reddit.get_subreddit("giftcardexchange")

	for submission in subreddit.get_new(limit=10):

		while not queue.empty():
			item = queue.get()
			comment(item[0], item[1])

		if vars(submission)["name"] not in already_done:
			author = vars(submission)["author"]
			comment_text = ""

			# Get account age
			author_created = datetime.datetime.fromtimestamp(int(author.created_utc))
			now = datetime.datetime.now()
			delta = now - author_created

			# Check if they're a scammer. If they are one, skip everything else and cut straight to the point.
			if author.name in scammers:
				comment_text += "**WARNING: THIS POSTER IS ON THE [CONFIRMED SCAMMERS LIST!](http://www.reddit.com/r/giftcardexchange/wiki/scammers)**\n\n\n***DO NOT, I REPEAT, DO NOT TRADE WITH THEM!***"
				comment(submission, comment_text)
				continue

			# Check if they're a good trader. If they are, skip everything else and cut straight to the point.
			if author.name in confirmed:
				comment_text += "**This poster is on the [Good Trader List!](http://www.reddit.com/r/giftcardexchange/comments/1wqwb9/trading_confirmation_thread_post_here_when_youve/)**\n\n\nThis means that they are safe to trade with!"
				comment(submission, comment_text)
				continue

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