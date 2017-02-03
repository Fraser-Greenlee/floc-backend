
# import webhook_key from tokens.py
from tokens import webhook_key

def verify(req):
	print req, webhook_key
	if 'hub.verify_token' in req and req['hub.verify_token'] == webhook_key:
		return req['hub.challenge']
	else:
		return 'bad request'
