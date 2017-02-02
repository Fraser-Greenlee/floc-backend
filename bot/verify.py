
def verify(req,token):
	print req
	if 'hub.verify_token' in req and req['hub.verify_token'] == token:
		return req['hub.challenge']
	else:
		return 'bad request'

#	/webhook?hub.mode=subscribe&hub.challenge=2077712982&hub.verify_token=messages
