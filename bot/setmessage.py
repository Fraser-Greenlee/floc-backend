
from fromat_current_msg import fromat_current_msg
import respond
from tokens import db

def setmessage(id,current_msg):
	# update database current_msg value
	db.query("UPDATE users SET current_msg='"+current_msg+"' WHERE id="+str(id))
	# call message function

	#	send to current message
	# -----------------------
	# get respond.py class from name
	current_class = getattr(respond, fromat_current_msg(current_msg))
	# call start method on message
	current_class.start(id)
