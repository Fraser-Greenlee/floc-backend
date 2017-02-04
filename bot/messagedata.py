import json

def msgfromraw(data):
	message = {}
	if 'text' in data:
		message['text'] = data['text']
	if 'attachments' in data:
		message['attachment'] = data['attachments'][0]
		if 'sticker_id' in data['attachments'][0]['payload']:
			return 'Err:sticker'

	return message

def messagedata(data):
	data = json.loads(data)
	try:
		id = int(data['entry'][0]['messaging'][0]['sender']['id'])
		message = msgfromraw(data["entry"][0]["messaging"][0]['message'])
		return {
			'id':id,
			'message':message
		}
	except Exception as e:
		print e
		return False
