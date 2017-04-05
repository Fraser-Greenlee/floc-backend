# -*- coding: utf-8 -*-
import grequests, requests, json, datetime, time

# import messagkey from tokens.py file
from tokens import access_token, TESTING, LOCAL_TEST

if LOCAL_TEST and TESTING:
	print 'Local Testing'
	URL = 'http://0.0.0.0:8888/'
else:
	print 'Not Testing'
	URL = 'https://graph.facebook.com/v2.6/me/messages'

def send(id, *messages, **args):
	messages = list(messages)
	print 'SENDING', '\n', time.time(), '\n', id, '\n', messages, '\n----------'
	for i in range(len(messages)):
		if type(messages[i]) != dict:
			messages[i] = {'text':messages[i]}
	if 'notify' in args:
		notifylist = args['notify']
	else:
		notifylist = []
	##
	if type(id) == list:
		# DELETE ME
		if len(notifylist) != len(id):
			print notifylist, '!=', id
			raise Exception('len(notifylist) != len(id)')
		#
		return sendList(id, messages, notifylist)
	else:
		sendSingle(id, messages)


def sendSingle(id, messages, notify=False):
	for message in messages:
		messageData = {
			'recipient': {
				'id': id
			},
			'message': message,
			'notification_type': ('SILENT_PUSH' if notify else 'NO_PUSH')
		}
		r = requests.post(
			URL,
			params = { 'access_token': access_token },
			json=messageData
		)
		if r.status_code != 200:
			if LOCAL_TEST or TESTING:
				raise Exception(str(json.loads(r._content)))
			else:
				print json.loads(r._content)

def sendList(idlist, messages, notifylist=[]):
	# make params for each request
	messageDataList = []
	has_nofifys = len(notifylist) > 0
	i = 0
	for i in range(len(idlist)):
		messageDataList += [{'recipient': {'id': idlist[i]}, 'message': message, 'notification_type':  'REGULAR' if has_nofifys and notifylist[i] else 'NO_PUSH'  } for message in messages]
	# DELETE ME
	print 'has_nofifys', has_nofifys
	print 'notifylist', notifylist
	print 'messageDataList', messageDataList
	#
	# make request list
	rs = (grequests.post(URL, params = {'access_token':access_token}, json=messageData) for messageData in messageDataList)
	# send all simultaneously
	start = datetime.datetime.now()
	resps = grequests.map(rs)
	print """
		Time to send:, """+str(datetime.datetime.now() - start)+"""
	"""
	# return responces in list
	return resps
