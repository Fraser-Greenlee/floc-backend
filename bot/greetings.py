import requests
from tokens import access_token


# Add/Remove Front page info
class Greeting:
	@staticmethod
	def add(message):
		message = {"text":message}
		r = requests.post(
			'https://graph.facebook.com/v2.6/me/thread_settings?access_token='+access_token,
			json={
				"setting_type":"greeting",
				"greeting": message
			}
		)
		if r.status_code != 200:
			raise Exception(json.loads(r._content)['error']['message'])
		else:
			return True

	@staticmethod
	def remove():
		r = requests.delete(
			'https://graph.facebook.com/v2.6/me/thread_settings?access_token='+access_token,
			json={"setting_type":"greeting"}
		)
		if r.status_code != 200:
			raise Exception(json.loads(r._content)['error']['message'])
		else:
			return True


# Add/Remove Get Started button
class Getstarted:
	@staticmethod
	def enable():
		r = requests.post(
			'https://graph.facebook.com/v2.6/me/thread_settings?access_token='+access_token,
			json={
			  "setting_type":"call_to_actions",
			  "thread_state":"new_thread",
			  "call_to_actions": [
					{
				    "payload": "GetStarted"
				  }
				]
			}
		)
		if r.status_code != 200:
			raise Exception(json.loads(r._content)['error']['message'])
		else:
			return True

	@staticmethod
	def disable():
		r = requests.delete(
			'https://graph.facebook.com/v2.6/me/thread_settings?access_token='+access_token,
			json={
				"setting_type":"call_to_actions",
				"thread_state":"new_thread"
			}
		)
		if r.status_code != 200:
			raise Exception(json.loads(r._content)['error']['message'])
		else:
			return True
