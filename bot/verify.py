# import webhook_key from tokens.py
from tokens import webhook_key

def verify(request):
	if 'hub.verify_token' in request.args and request.args['hub.verify_token'] == webhook_key:
		return request['hub.challenge']
	else:
		return 'webhook failed'
