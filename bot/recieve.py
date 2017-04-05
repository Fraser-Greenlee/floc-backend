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
	for entry in data:#entry = data[0]
		li = entry['messaging']
		for messaging in li:#messaging = li[0]
			v = recieveVal(messaging, sess)
			if v not in [None,False]:
				sess, msg = v
				# send return to user if str
				if type(msg) in [str,unicode]:
					send(sess.id,msg)


def handleQuickReply(messaging, sess):
	payload = messaging['message']['quick_reply']['payload']
	if ':' in payload:
		l = payload.split(':')
		fn_name, args = l[0], l[1:]
		return getattr(responces, fn_name)(sess, args)
	else:
		return getattr(responces, payload)(sess)


def frompast(sess,timestamp):
	if sess.last_sent >= timestamp:
		print '* PAST *'
		return True
	else:
		sess.update_db(last_sent=timestamp)
		return False


def handleMsg(messaging, sess):
	# manage users in database
	id = messaging["sender"]["id"]
	q = db.select('users', where="id="+str(id))
	if len(q) == 0:
		return new_user(sess,id)
	else:
		r = q[0]
		sess.set_dict(r)
	# Check not from past
	if frompast(sess, messaging['timestamp']):
		return sess, False
	# handle quick reply
	if 'quick_reply' in messaging['message']:
		return handleQuickReply(messaging, sess)
	# send to current message
	else:
		return getattr(responces, sess.current_msg+'_msg')(sess, messaging)


def recieveVal(messaging, sess):
	print 'recieveVal', messaging
	if 'message' in messaging and ('is_echo' not in messaging['message'] or messaging['message']['is_echo'] is False):
		return handleMsg(messaging, sess)
	# if new Get Started message
	elif "postback" in messaging and messaging["postback"]["payload"] == "GetStarted":
		return new_user(sess,messaging["sender"]["id"])
	# update relevent cols for read and delivery msgs
	elif 'read' in messaging:
		db.query("UPDATE users SET notified=false, last_read="+str(messaging['read']['watermark'])+" WHERE id="+str(messaging["sender"]["id"]))
		return sess, False
	elif 'delivery' in messaging:
		db.query("UPDATE users SET last_recieved="+str(messaging['delivery']['watermark'])+" WHERE id="+str(messaging["sender"]["id"]))
		return sess, False
	else:
		raise Exception("input is neither postback or message")


def new_user(sess,id):
	print id
	db.query("DELETE from users where id="+str(id))
	db.insert('users',id=id)
	sess.id = id
	sess.new_user = True
	return responces.Start_msg(sess, "x")
