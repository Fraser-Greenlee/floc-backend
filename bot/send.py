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

def send(id, *messages, **suggest):
	messages = list(messages)
	print 'SENDING', '\n', time.time(), '\n', id, '\n', messages, '\n----------'
	for i in range(len(messages)):
		if type(messages[i]) != dict:
			messages[i] = {'text':messages[i]}
	#
	suggests = []
	if 'suggest' in suggest and suggest['suggest'] is not False:
		print 'suggest:', suggest
		if suggest['suggest'] == '$location':
			messages[-1]['quick_replies'] = [{"content_type":"location"}]
		else:
			messages[-1]['quick_replies'] = [
				{
	        "content_type":"text",
	        "title":reply[0],
	        "payload":reply[1]
				}
				for reply in suggest['suggest']
			]
	elif 'suggests' in suggest:
		suggests = suggest['suggests']
	##
	if type(id) == list:
		return sendList(id, messages, suggests)
	else:
		sendSingle(id, messages)


def sendSingle(id, messages):
	for message in messages:
		messageData = {
			'recipient': {
				'id': id
			},
			'message': message,
			'notification_type': 'NO_PUSH'
		}
		print 'messageData', messageData
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

def load_quick_reply(qr):
	return json.loads(qr.replace("''","'").replace("u'","'").replace("'",'"'))

def sendList(idlist, messages, suggests):#idlist, message = [[1166543533459050L],{'text':'hello'}]
	# make params for each request
	messageDataList = []
	i = 0
	for id in idlist:
		if suggests != []:
			print suggests, i
			# suggestions
			if suggests[i] is not None:
				messages[-1]['quick_replies'] = [
					{
		        "content_type":"text",
		        "title":reply[0],
		        "payload":reply[1]
					}
					for reply in load_quick_reply(suggests[i])
				]
			i += 1
		messageDataList += [{'recipient': {'id': id}, 'message': message, 'notification_type': 'NO_PUSH'} for message in messages]
	print 'messageDataList', messageDataList
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
