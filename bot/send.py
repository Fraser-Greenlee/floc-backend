# -*- coding: utf-8 -*-
import requests
import json

# import messagkey from tokens.py file
from tokens import access_token
from error import SendError

def send(id, message):
	messageData = {
		'recipient': {
			'id': id
		},
		'message': message,
		'notification_type': 'NO_PUSH'
	}
	r = requests.post(
		'https://graph.facebook.com/v2.6/me/messages',
		params = { 'access_token': access_token },
		json=messageData
	)
	if r.status_code != 200:
		print messageData
		raise SendError(json.loads(r._content)['error'])
#
