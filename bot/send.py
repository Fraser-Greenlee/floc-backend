
import requests
import json

id = 1399267706750548
msg = 'test'

def send(id,msg,**options):
	messageData = {
		'recipient': {
			'id': id
		},
		'message': {
			'text': msg
		}
	}
	r = requests.post(
		'https://graph.facebook.com/v2.6/me/messages',
		params = { 'access_token': 'EAAXOp7BV89QBAK7mDazR9WwA8ZAQZA4e2hD31jTZCZCqyZBQFkn9afPHGUrcNlkFLxpZCxKbWOAkI5rnLv24Ox7QycuarT2CXmAoSsH6aZB2t36JJypxHrR5OjJIqP5KGxREHWZB3juiZArbIhdZA1J57psSf4ldaUdhXnJbnLPIdZAbgZDZD' },
		json=messageData
	)
	if r.status_code == 200:
		print("Successfully sent generic message!");
	else:
		print(json.loads(r._content)['error']);


#	my id: 1399267706750548
