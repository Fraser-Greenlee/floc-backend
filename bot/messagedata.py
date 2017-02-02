
import json

def messagedata(data):
	data = json.loads(data)
	try:
		id = data['entry'][0]['messaging'][0]['sender']['id']
		message = data["entry"][0]["messaging"][0]['message']['text']
		return {
			'id':id,
			'message':message
		}
	except Exception as e:
		print e
		return False
