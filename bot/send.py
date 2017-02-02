
import requests
import json

# import messagkey from tokens.py file
from tokens import access_token

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
		params = { 'access_token': access_token },
		json=messageData
	)
	if r.status_code == 200:
		print("Successfully sent generic message!");
	else:
		print(json.loads(r._content)['error']);
