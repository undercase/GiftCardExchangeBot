import praw
import datetime
import time

reddit = praw.Reddit("GiftCardExchange Warner v1.0 by /u/superman3275",)
reddit.login()

already_done = []

while True:

	subreddit = reddit.get_subreddit("giftcardexchange")

	for submission in subreddit.get_new(limit=10):

		if not (submission in already_done):
			author = vars(submission)["author"]
			comment = ""

			# Get account age
			author_created = datetime.datetime.fromtimestamp(int(author.created_utc))
			now = datetime.datetime.now()
			delta = now - author_created

			# Check account age
			if delta.days < 7:
				comment +=  "WARNING: THIS ACCOUNT IS LESS THAN A WEEK OLD! TRADE WITH CAUTION!\n\n\n"
			elif delta.days < 31:
				comment += "WARNING: THIS ACCOUNT IS LESS THAN A MONTH OLD! TRADE WITH CAUTION!\n\n\n"
			elif delta.days < 93:
				comment += "WARNING: THIS ACCOUNT IS LESS THAN THREE MONTHS OLD! TRADE WITH CAUTION!\n\n\n"
			else:
				comment += "THIS USER'S ACCOUNT IS OLDER THAN THREE MONTHS! SO FAR, IT LOOKS SAFE!\n\n\n"

			# Check comment karma
			if author.comment_karma < 10:
				comment += "WARNING: THIS USER HAS VERY, VERY LITTLE KARMA! TRADE WITH CAUTION!\n\n\n"
			elif author.comment_karma < 100:
				comment += "WARNING: THIS USER HAS LITTLE KARMA! TRADE WITH CAUTION!\n\n\n"
			elif author.comment_karma < 300:
				comment += "WARNING: THIS USER HAS LESS-THAN-AVERAGE KARMA! TRADE WITH CAUTION!\n\n\n"
			else:
				comment += "THIS USER HAS MORE THAN 300 KARMA! IT LOOKS SAFE!\n\n\n"

			# Overall
			count = sentence.count("WARNING")
			if count == 2:
				comment += "OVERALL: DO NOT TRADE WITH THIS PERSON! THEY DO NOT HAVE AN OLD ENOUGH ACCOUNT OR ENOUGH KARMA!"
			elif count == 1:
				comment += "OVERALL: BE CAREFUL WITH THIS PERSON! THEY ONLY FULFILL ONE OF THE SUBREDDIT REQUIREMENTS!"
			elif count == 0:
				comment += "OVERALL: THIS PERSON'S ACCOUNT LOOKS GREAT!"

			submission.add_comment(comment)

			already_done.append(submission)
	time.sleep(30)