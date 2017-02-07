import respond, json
from tokens import db
from error import SendError

def recieve(data):
	data = json.loads(data)
	try:
		data = data['entry']
	except Exception as e:
		print "Bad message json.", e
		return False
	#
	for entry in data:#entry = data[0]
		try:
			li = entry['messaging']
			for info in li:#info = li[0]
				try:
					recieveVal(info)
				except Exception as e:
					print "recieveVal error,", str(e)
		except Exception as e:
			print "Bad entry json.", e
	#


def recieveVal(info):
	# sort postback from message
	id = info["sender"]["id"]
	if "message" in info:
		message = info["message"]

		if "is_echo" in message and message["is_echo"]:# if is_echo ignore it
			return False

		# manage user in database
		q = db.query("SELECT current_msg FROM users WHERE id="+str(id))
		if len(q) == 0:
			# new user
			db.query("INSERT INTO users (id,current_msg) VALUES ("+str(id)+",'start')")
			current_msg = 'Start'
		else:
			current_msg = q[0]['current_msg']
			current_msg = current_msg[0].upper()+current_msg[1:]# Start from start

		##	send to current message
		# get respond.py class from name
		current_class = getattr(respond, current_msg)
		# call recieve method on message
		current_class.recieve(id,message)
		return 'True'
	#
	elif "postback" in info:
		key = info["postback"]["payload"]
		if key == "GetStarted":
			# is a new user
			db.query("DELETE FROM users WHERE id="+str(id))
			db.query("INSERT INTO users (id,current_msg) VALUES ("+str(id)+",'start')")
			# set to start and send there
			respond.Start.recieve(id, 'Get Started')
	#
	elif "read" in info or "delivery" in info:
		# user has read message
		return False
	else:
		raise Exception("input is neither postback or message")
