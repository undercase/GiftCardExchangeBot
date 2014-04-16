import praw
import datetime
import time
import getpass
import gspread

overall = {
	0: "This is a great poster! They have an established account and lots of karma! (Still be careful though)",
	1: "This is a good poster! They have a relatively established account.",
	2: "This is a okay poster! They have a somewhat established account.",
	3: "This is a slightly risky poster! Be careful when trading.",
	4: "This is a risky poster! Be very careful when trading.",
	5: "This is a very risky poster! Be extremely careful when trading.",
	6: "This is a **very, very high risk** poster! Be careful when trading."
}

spreadsheet_url = "https://docs.google.com/spreadsheet/ccc?key=0AiFZyanaAvZDdHdyS0dQMnRSY01HVWYzSldTaGowbXc#gid=0"

def gspread_input_login():
	username = raw_input("Username: ")
	password = getpass.getpass()
	return gspread.login(username, password)

# Exit function to save already_done
def save_already_done():
	with open("already_done.txt", "w") as done:
		for line in range(len(already_done) - 10, len(already_done)):
			# This ternary operator makes sure a newline isn't added on the last line.
			done.write(already_done[line] + ("\n" if line == len(already_done) else ""))

def comment(submission, comment_text, donate=True):
	global already_done
	if donate:
		comment_text += "\n\n\n[^Donate ^to ^the ^Creator ^of ^this ^Bot ^(Please)^!](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=A3HSK4BPG56BU)"
	try:
		if submission.name not in already_done:
			submission.add_comment(comment_text)
			already_done.append(submission.name)
			print "Commented on submission " + submission.name
	except praw.errors.RateLimitExceeded as error:
		print "Submission: " + submission.name + " commenting failed! Sleeping for %d seconds!" % error.sleep_time
		time.sleep(error.sleep_time)
		comment(submission, comment_text, donate=False)

def main():

	gc = gspread_input_login()

	spreadsheet = gc.open_by_url(spreadsheet_url)
	worksheet = spreadsheet.worksheet("Ban List")

	banned = worksheet.col_values(1)

	while True:

		subreddit = reddit.get_subreddit("giftcardexchange")

		for submission in subreddit.get_new(limit=10):

			if submission.name not in already_done:
				author = submission.author
				comment_text = ""
				rating = 0

				# Get account age
				author_created = datetime.datetime.fromtimestamp(int(author.created_utc))
				now = datetime.datetime.now()
				delta = now - author_created

				# Check if they're a scammer. If they are one, skip everything else and cut straight to the point.
				if author.name in scammers or author.name in banned:
					comment_text += "**WARNING: THIS POSTER IS ON THE [CONFIRMED SCAMMERS LIST!](http://www.reddit.com/r/giftcardexchange/wiki/scammers)**\n\n\n***DO NOT, I REPEAT, DO NOT TRADE WITH THEM!***"
					comment(submission, comment_text)
					continue

				# Check if they're a good trader. If they are, skip everything else and cut straight to the point.
				if author.name in confirmed:
					comment_text += "**This poster is on the [Good Trader List!](http://www.reddit.com/r/giftcardexchange/comments/1wqwb9/trading_confirmation_thread_post_here_when_youve/)**\n\n\nThis means that they are safe to trade with!"
					comment(submission, comment_text)
					continue

				# Check account age
				if delta.days <= 1:
					rating += 3
					comment_text +=  "WARNING: This poster's account is less than a day old (EXTREMELY RISKY)! Trade with caution!\n\n\n"
				elif delta.days <= 7:
					rating += 2
					comment_text += "WARNING: This poster's account is less than a seven days old (VERY RISKY)! Trade with caution!\n\n\n"
				elif delta.days <= 31:
					rating += 1
					comment_text += "WARNING: This poster's account is less than a month old (RISKY)! Trade with caution!\n\n\n"
				else:
					comment_text += "This poster's account is older than a month! It is established on reddit!\n\n\n"

				# Check comment karma
				if author.comment_karma < 10:
					rating += 3
					comment_text += "WARNING: This poster has very, very little (less than ten) karma! Trade with caution!\n\n\n"
				elif author.comment_karma < 50:
					rating += 2
					comment_text += "WARNING: This poster has little (less than fifty) karma! Trade with caution!\n\n\n"
				elif author.comment_karma < 100:
					rating += 1
					comment_text += "WARNING: This poster has less-than-average (less than one-hundred) karma! Trade with caution!\n\n\n"
				else:
					comment_text += "This poster has more than one-hundred karma! (S)he has earned a fair amount of karma!\n\n\n"

				# Overall
				comment_text += overall[rating]
				
				comment(submission, comment_text)
		time.sleep(1800)

# Ensure that the bot won't be automatically executed when being imported
if __name__ == "__main__":

	reddit = praw.Reddit("GiftCardExchange Warner v2.0 by /u/superman3275",)
	reddit.login()

	# Generate already_done list
	with open("already_done.txt", "r") as done:
		already_done = done.readlines()
	for line in range(len(already_done)):
		already_done[line] = already_done[line].strip()
	# Generate scammers list
	with open("scammers.txt", "r") as scammer:
		scammers = scammer.readlines()
	for scammer in range(len(scammers)):
		scammers[scammer] = scammers[scammer].strip()
	# Generate confirmed traders list
	with open("confirmed.txt", "r") as confirm:
		confirmed = confirm.readlines()
	for confirm in range(len(confirmed)):
		confirmed[confirm] = confirmed[confirm].strip()

	main()