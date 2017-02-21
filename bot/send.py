# -*- coding: utf-8 -*-
import grequests, requests, json
import datetime

# import messagkey from tokens.py file
from tokens import access_token
from error import SendError

def send(id, message):
	if type(message) == str:
		message = {'text':unicode(message, 'utf-8')}
	if type(id) == list:
		return sendList(id, message)
	else:
		sendSingle(id, message)


def sendSingle(id, message):
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
		raise SendError(json.loads(r._content)['error'])


def sendList(idlist, message):#idlist, message = [[1166543533459050L],{'text':'hello'}]
	# make params for each request
	messageDataList = [{'recipient': {'id': id}, 'message': message, 'notification_type': 'NO_PUSH'} for id in idlist]
	# make request list
	rs = (grequests.post('https://graph.facebook.com/v2.6/me/messages', params = {'access_token':access_token}, json=messageData) for messageData in messageDataList)
	# send all simultaneously
	start = datetime.datetime.now()
	resps = grequests.map(rs)
	print ' '
	print 'Time to send:', (datetime.datetime.now() - start)
	print ' '
	# return errors in list
	errors = []
	for r in resps:
		if r.status_code != 200:
			print 'Send Error:', json.loads(r._content)['error']
			errors.append(json.loads(r._content)['error'])
	return errors
#

#	heroku addons:attach my-originating-app::DATABASE --secret-messenger
