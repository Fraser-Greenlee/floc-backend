import json

def recieve(web_data):
	print 'recieving...'
	jsn = json.loads(web_data)
	# test message structure
	try:
		from_id = jsn['recipient']['id']
		print 'FROM:', from_id
		msg = jsn['message']
		if 'text' not in msg:
			if 'attachment' in msg:
				attachment = msg['attachment']
				if attachment['type'] not in ['image','audio','video','file']:
					raise Exception('weird type '+str(attachment['type']))
				if 'payload' not in attachment:
					return 'Error: no payload in attachment'
		elif 'quick_replies' in msg:
			if len(msg['quick_replies']) == 0:
				raise Exception('Too few quick_replies')
	except Exception as e:
		print 'Recieve Error: '+str(e)
		return 'Error: message structure. '+str(jsn)
	# save message
	f = open('messages/'+str(from_id)+'.json', 'r')
	data = json.loads(f.read())
	data['messages'].append(jsn)# append whole request
	data['checked_last'] = False
	f = open('messages/'+str(from_id)+'.json', 'w')
	f.write(json.dumps(data))
	print 'Saved to '+str(from_id)+'.json:', data
	return ''
