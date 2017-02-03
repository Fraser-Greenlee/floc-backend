
from messagedata import messagedata
from fromat_current_msg import fromat_current_msg
import respond
from tokens import db

def recieve(data):
	data = messagedata(data)
	if data:
		id = data['id']
		message = data['message']

		# manage user in database
		q = db.query("SELECT current_msg FROM users WHERE id="+str(id))
		if len(q) == 0:
			# new user
			db.query("INSERT INTO users (id,current_msg) VALUES ("+str(id)+",'start')")
			current_msg = 'Start'
		else:
			current_msg = fromat_current_msg(q[0]['current_msg'])


		#	send to current message
		# -----------------------
		# get respond.py class from name
		current_class = getattr(respond, current_msg)
		# call recieve method on message
		current_class.recieve(id,message)
		return 'True'

	else:
		return 'Bad sent data.'
