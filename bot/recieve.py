import responces, json
from tokens import db
from error import SendError
from bot.send import send

def recieve(data, sess):
	data = json.loads(data)
	try:
		data = data['entry']
	except Exception as e:
		print "Bad message json.", e
		return False
	#
	for entry in data:#entry = data[0]
		li = entry['messaging']
		for info in li:#info = li[0]
			sess, msg = recieveVal(info, sess)
			# send return to user if str
			if type(msg) == str:
				send(sess.id,msg)
#


def recieveVal(info, sess):
	# sort postback from message
	id = info["sender"]["id"]
	if "message" in info:
		message = info["message"]

		# if is_echo ignore it
		if "is_echo" in message and message["is_echo"]:
			return sess, False

		# manage users in database
		q = db.select('users', where="id="+str(id))
		if len(q) == 0:
			# insert sess vars
			sess.id = id
			db.query("INSERT INTO users (id) VALUES ("+str(id)+")")
		else:
			# set sess vars (without updating database)
			sess.set_dict(q[0])

		#	send to current message
		send_fn = getattr(responces, sess.current_msg+'_msg')
		return sess, send_fn(sess, message)
	#
	elif "postback" in info:
		key = info["postback"]["payload"]
		if key == "GetStarted":
			# is a new user
			db.query("DELETE FROM users WHERE id="+str(sess.id))
			db.query("INSERT INTO users (id,current_msg) VALUES ("+str(sess.id)+",'start')")
			# set to start and send there
			responces.Start_msg(sess, 'Get Started')
	#
	elif "read" in info or "delivery" in info:
		# user has read message
		return sess, False
	else:
		raise Exception("input is neither postback or message")
