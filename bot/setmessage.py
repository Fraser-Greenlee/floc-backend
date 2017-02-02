
import respond

def setmessage(db,id,name):
	# update database current_msg value
	db.query("UPDATE users SET current_msg='"+name+"' WHERE userid="+str(id))
	# call message function
