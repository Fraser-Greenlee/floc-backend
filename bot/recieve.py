import responces, json
from tokens import db, TESTING, LOCAL_TEST
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
			v = recieveVal(info, sess)
			if v not in [None,False]:
				sess, msg = v
				# send return to user if str
				if type(msg) in [str,unicode]:
					send(sess.id,msg)
#


def recieveVal(info, sess):
	# sort postback from message
	id = info["sender"]["id"]
	# Check not from past
	if 'timestamp' in info:
		q = db.query("SELECT last_time from users where id="+str(id))
		if len(q) > 0:
			if q[0]['last_time'] >= info['timestamp']:
				if LOCAL_TEST:
					print '* PAST *'
					print info
					print '* ---- *'
				return False
			else:
				db.update('users',where="id="+str(id),last_time=info['timestamp'])
	#
	if "message" in info:
		message = info["message"]

		# if is_echo ignore it
		if "is_echo" in message and message["is_echo"]:
			return sess, False

		# manage users in database
		q = db.select('users', where="id="+str(id))
		if len(q) == 0:
			return new_user(sess,id)
		else:
			# set sess vars (without updating database)
			r = q[0]
			sess.set_dict(r)
			if r['location'] is not None:
				sess.set(
					lat=float(r['location'][1:r['location'].index(',')]),
					long=float(r['location'][r['location'].index(',')+1:-1])
				)

		# if quick reply send to payload as function
		if 'quick_reply' in message:
			payload = message['quick_reply']['payload']
			if ':' in payload:
				l = payload.split(':')
				fn_name, args = l[0], l[1:]
				return getattr(responces, fn_name)(sess, args)
			else:
				return getattr(responces, payload)(sess)

		#	send to current message
		send_fn = getattr(responces, sess.current_msg+'_msg')
		return send_fn(sess, message)
	#
	elif "postback" in info and info["postback"]["payload"] == "GetStarted":
		return new_user(sess,id)
	#
	elif "read" in info or "delivery" in info:
		# user has read message
		return sess, False
	else:
		raise Exception("input is neither postback or message")

def new_user(sess,id):
	sess.id = id
	db.delete('users',where='id='+str(sess.id))
	db.insert('users',id=sess.id)
	sess.new_user = True
	return responces.Start_msg(sess, "x")
