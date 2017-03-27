from os import listdir, makedirs
from os.path import isfile, join, exists
import json, requests, random, string, time
import testbot

DELAY = 1.1

def getusers():
	return [int(f[:f.index('.')]) for f in listdir('messages/')]

def new_json_file(id):
	print 'new', str(id)+'.json'
	open('messages/'+str(id)+'.json', 'w').write(json.dumps({'checked_last':False,'messages':[]}))
	time.sleep(DELAY)

def random_id():
	return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

def mid(self):
	return "mid." + random.choice([
		'$'+''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(29)),
		str(self.time())+":"+random_id()
	])

class User:
	def __init__(self,*id):
		if not exists('messages/'):
			makedirs('messages/')
		self.time_offset = 0
		if len(id) is 0:
			# random new id
			users = getusers()
			id = 1
			while id in users:
				id+=1
			self.id = id
			print 'x', id
			new_json_file(id)
		else:
			# assign set id
			id = id[0]
			self.id = id
			if id not in getusers():
				print 'y', id
				new_json_file(id)

	def time(self):
		return testbot.timestamp() + self.time_offset

	def read(self):
		return json.load(open('messages/'+str(self.id)+'.json','r'))

	def write(self,data):
		open('messages/'+str(self.id)+'.json', 'w').write(json.dumps(data))

	def checked_last(self):
		return self.read()['checked_last']

	def messages(self):
		return self.read()['messages']

	def last_msg(self):
		return self.messages()[-1]

	def _received_txt(self,msg,last_msg):
		try:
			if type(msg) != unicode:
				msg = unicode(msg, 'utf-8')
			txt = last_msg['message']['text']
			return [msg == txt,msg,txt]
		except Exception as e:
			print 'Text Message Error:', str(e)
			return [False, msg, '$Err: Couldn\'t open text message.']

	def _received_attachment(self,msg,last_msg):
		try:
			attachment = last_msg['message']['attachment']
			return [attachment['type'] == msg['type'] and attachment['payload']['url'] == msg['payload']['url'], msg, attachment]
		except Exception as e:
			print 'Attachment Message Error:', str(e)
			return [False, msg, '$Err: Couldn\'t open attachment.']

	def _received_suggestions(self,suggestions,last_msg):
		try:
			quick_replies = last_msg['message']['quick_replies']
			print 'old replies:', quick_replies
			all_correct = True
			for i in range(len(suggestions)):
				if quick_replies[i]['title'] != suggestions[i]:
					all_correct = False
			return [True, quick_replies, suggestions]
		except Exception as e:
			print 'Suggestions Error:', str(e)
			return [False, suggestions, quick_replies]

	def did_receive(self,*msgs,**suggest):
		time.sleep(DELAY)
		if self.checked_last():
			return testbot.addresult([False, msgs, '$Nothing New'])
		if len(self.messages()) is 0:
			return testbot.addresult([False, msgs, '$Nothing'])
		#
		data = self.read()
		data['checked_last'] = True
		self.write(data)
		#
		offset = len(msgs)
		for msg in msgs:
			try:
				last_msg = self.messages()[-offset]
			except:
				print 'Offset Message Error:', str(e)
				res = [False,msg,'$Err: Offset Message Error.']
				break
			#
			if type(msg) in (str,unicode):
				res = self._received_txt(msg,last_msg)
			else:
				print '_received_attachment', msgs, msg
				res = self._received_attachment(msg,last_msg)
			#
			if res[0] is False:
				return testbot.addresult(res)
			offset-=1
		# only check suggestions on most recent message
		if 'suggest' in suggest:
			res = self._received_suggestions(suggest['suggest'],last_msg)
		#
		return testbot.addresult(res)
	#

	def quick_reply(self,key):
		time.sleep(DELAY)
		quick_replies = self.last_msg()['message']['quick_replies']
		for reply in quick_replies:
			if reply[u'title'] == unicode(key):
				time.sleep(DELAY)
				requests.post(
					testbot.send_to,
					json={
						"object":"page",
						"entry":[
							{
								"id": testbot.page_id,
								"time":self.time(),
								"messaging":[
									{
									  "sender": {
									    "id": self.id
									  },
									  "recipient": {
									    "id": testbot.page_id
									  },
									  "timestamp":self.time(),
									  "message": {
									    "mid" : mid(self),
									    "text": reply['title'],
									    "quick_reply": {
									      "payload": reply['payload']
									    }
								  	}
									}
								]
							}
						]
					}
				)
				return True

	def postback(self,key):
		time.sleep(DELAY)
		requests.post(
			testbot.send_to,
			json={
				"object":"page",
				"entry":[
					{
						"id": testbot.page_id,
						"time":self.time(),
						"messaging":[
							{
								"sender":{
									"id":self.id
								},
								"recipient":{
									"id": testbot.page_id
								},
								"timestamp":self.time(),
								"postback":{
									"payload":key
								}
							}
						]
					}
				]
			})

	def sendlocation(self,**coords):
		time.sleep(DELAY)
		if 'lat' not in coords:
			coords['lat'] = -85.0
		if 'long' not in coords:
			coords['long'] = 0.0
		#
		requests.post(
			testbot.send_to,
			json={
				"object":"page",
				"entry":[
					{
						"id": testbot.page_id,
						"time":self.time(),
						"messaging":[
							{
								"sender":{
									"id":self.id
								},
								"recipient":{
									"id": testbot.page_id
								},
								"timestamp":self.time(),
								"message":{
									"mid":mid(self),
									"attachments":[
										{
											"title":"$name location",
											'url':'Not done.',
											"type":'location',
											"payload":{
												'coordinates': {
													'lat':coords['lat'],
													'long':coords['long']
												}
											}
										}
									]
								}
							}
						]
					}
				]
			})
	#

	def send(self,data):
		time.sleep(DELAY)
		if type(data) == str:
			requests.post(
				testbot.send_to,
				json={
					"object":"page",
					"entry":[
						{
							"id": testbot.page_id,
							"time":self.time(),
							"messaging":[
								{
									"sender":{
										"id":self.id
									},
									"recipient":{
										"id": testbot.page_id
									},
									"timestamp":self.time(),
									"message":{
										"mid":mid(self),
										"text":data
									}
								}
							]
						}
					]
				})
		else:
			jsn = {
				"object":"page",
				"entry":[
					{
						"id": testbot.page_id,
						"time":self.time(),
						"messaging":[
							{
								"sender":{
									"id":self.id
								},
								"recipient":{
									"id": testbot.page_id
								},
								"timestamp":self.time(),
								"message":{
									"mid":mid(self),
										"attachments":[
																		{
																			"type":data['type'],
																			"payload":{
																				"url":data['payload']['url']
																			}
																		}
																	]
								}
							}
						]
					}
				]
			}
			if 'text' in data:
				jsn['entry'][0]['messaging'][0]['message']['text'] = data['text']
			requests.post( testbot.send_to, json=jsn )
#
