# -*- coding: utf-8 -*-
import requests
import json

# import messagkey from tokens.py file
from tokens import access_token

def send(id,message,**options):
	if type(id) == list:
		lid = id
		for id in lid:
			send(id,message)
	else:
		messageData = {
			'recipient': {
				'id': id
			},
			'message': message
		}
		print "SEND"
		print messageData
		r = requests.post(
			'https://graph.facebook.com/v2.6/me/messages',
			params = { 'access_token': access_token },
			json=messageData
		)
		if r.status_code == 200:
			print("sent message");
		else:
			print {'messageData':messageData, 'error json':json.loads(r._content)['error']}
			raise Exception("Message failed:", json.loads(r._content)['error']['message'])
