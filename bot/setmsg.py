import responces

def setmsg(sess, new_msg):
	new_msg = new_msg[0].upper() + new_msg[1:]
	sess.set(current_msg=new_msg)
	# return _start variable if present
	if hasattr(responces, new_msg+'_start'):
		return getattr(responces, new_msg+'_start')