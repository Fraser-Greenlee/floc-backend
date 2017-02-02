
import respond
import json

def recieve(data,db):
	data = json.loads(data)
	try:
		id = data['entry'][0]['messaging'][0]['sender']['id']
		message = data["entry"][0]["messaging"][0]['message']['text']

		# manage user in database
		q = db.query("SELECT current_msg FROM users WHERE userid="+str(id))
		if len(q) == 0:
			# new user
			db.insert('users',userid=int(id),current_msg='start')
			current_msg = 'start'
		else:
			current_msg = q[0]['current_msg']


		#	send to current message
		# -----------------------
		# get respond.py class from name
		current_class = getattr(respond, current_msg)
		# call recieve method on message
		current_class.recieve(db,id,message)
		return 'True'

	except Exception as e:
		print e
		return 'Bad sent data.'
