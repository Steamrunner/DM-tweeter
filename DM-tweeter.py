#!/usr/bin/env python

"""
This script listens to direct messages and tweets them when sender is found in a list.
"""

from _common import get_api
import tweetpony

# file containing list of authorised twitter accounts
WHITELIST = "whitelist"

class StreamProcessor(tweetpony.StreamProcessor):
	def on_message(self, message):
		print "Message received from @%s: %s" % (message.sender_screen_name, message.text)

		api = get_api()
		screen_name = "@" + message.sender_screen_name
		text = message.text + " (" + screen_name + ")"

		lines = [line.strip() for line in open(WHITELIST)]

		if any(screen_name in s for s in lines):
			print("User authorised")
			try:
    				#api.update_status(status = text)
				print(text)
			except tweetpony.APIError as err:
			    print "Twitter returned error #%i and said: %s" % (err.code, err.description)
			else:
			    print "Tweet send"
		else:
			print("User not authorised")

		return True

def main():

	api = get_api()
	if not api:
		return
	processor = StreamProcessor(api)
	try:
		api.user_stream(processor = processor)
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	main()
