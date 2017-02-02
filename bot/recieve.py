
import respond
from messagedata import messagedata


def recieve(data,db):
	data = messagedata(data)
	if data:
		id = data['id']
		message = data['message']

		# manage user in database
		q = db.query("SELECT current_msg FROM users WHERE userid="+str(id))
		if len(q) == 0:
			# new user
			db.insert('users',userid=int(id),current_msg='start')
			current_msg = 'Start'
		else:
			current_msg = q[0]['current_msg'][0].upper()+q[0]['current_msg']


		#	send to current message
		# -----------------------
		# get respond.py class from name
		current_class = getattr(respond, current_msg)
		# call recieve method on message
		current_class.recieve(db,id,message)
		return 'True'

	else:
		return 'Bad sent data.'
