import responces

def setmsg(sess, new_msg):
	new_msg = new_msg[0].upper() + new_msg[1:]
	sess.update(current_msg=new_msg)
	# return _start variable if present
	if hasattr(responces, new_msg+'_start'):
		return sess, getattr(responces, new_msg+'_start')
