# -*- coding: utf-8 -*-
import datetime
import bot, random, re, web, time, json
from emojis import emojis
from tokens import db, TESTING, LOCAL_TEST

#### Handle Special Actions

def active(sess):
	# emojis of users who read a message within 3 minuets of the most recent message
	return u''.join( [emojis[r['identity']] for r in db.query("SELECT identity from users where notified=false")] )

def reset(sess):
	print 'reset', sess.last_reset
	delta = datetime.datetime.combine(datetime.date.today(), datetime.datetime.time(datetime.datetime.now())) - datetime.datetime.combine(datetime.date.today(), sess.last_reset)
	if (delta.seconds / 60) < 10:
		return [u'Must wait 10 minuets between resets.', sess]
	sess = set_identity(sess)
	group_msg(sess, "Added", reverse=True)
	sess.update_db(last_reset='now()')
	return [u'You are now '+emojis[sess.identity], sess]

def me(sess):
	return u'You are '+emojis[sess.identity]

def special_cases(sess,text):
	if text[0] == '@':
		if text == '@active':
			ret = active(sess)
		elif text == '@reset':
			ret, sess = reset(sess)
		elif text == '@me':
			ret = me(sess)
		elif text == '@actions':
			ret = u'@active, see active users\n@reset, reset your emoji\n@me, see your current emoji'
		else:
			ret = u'Not an action\nTo see all actions send "@actions"'
		return sess, ret
	else:
		return False

## Check Text

def check_text(sess,text):
	if len(text) > 200:
		return 'Not sent.\nMessage must be under 200 characters.'
	elif len(text.split('\n'))-1 >= 5:
		return 'Not sent.\nMessage has too many new lines.'

#

def set_identity(sess):
	sess.update(identity=db.query("""
		SELECT s
		FROM generate_series(1, 241) s
		WHERE s NOT IN (SELECT identity FROM users)
		order by s asc limit 1
	""")[0]['s'])
	return sess

##

def group_msg(sess,msg,**args):
	if type(msg) == str:
		msg = unicode(msg,'utf-8')
	if type(msg) == unicode:
		msg = {u'text':msg}
	#
	if 'mid' in msg and 'seq' in msg:
		del msg['mid']
		del msg['seq']
	#
	q = list(db.query("SELECT id, notified, last_read FROM users WHERE recieve_messages=true AND id<>"+str(sess.id)))
	#
	db.query("UPDATE users SET notified=true WHERE recieve_messages=true AND id<>"+str(sess.id))
	notifylist = [r['notified'] is False for r in q]
	#
	ids = [r['id'] for r in q]
	#
	if 'attachments' in msg:
		msg['attachment'] = msg['attachments'][0]
		del msg['attachments']
		if 'text' in msg:
			nmsg = dict(msg)
			del nmsg['text']
			responces = bot.send(ids, emojis[sess.identity]+u' '+unicode(msg['text']), nmsg, notify=notifylist)
		else:
			responces = bot.send(ids, emojis[sess.identity], msg, notify=notifylist)
	else:
		if 'reverse' in args and args['reverse']:
			txt = unicode(msg['text'])+u' '+emojis[sess.identity]
		else:
			txt = emojis[sess.identity]+u' '+unicode(msg['text'])
		#
		responces = bot.send(ids, txt, notify=notifylist)
	sent_responces(responces,ids)
	#
	return sess

def sent_responces(responces,ids):
	i=0
	for resp in responces:
		if resp.status_code != 200:
			print 'resp._content', resp._content
			j = json.loads(resp._content)
			if 'error' in j and 'code' in j['error'] and j['error']['code'] == 200 and 'error_subcode' in j['error'] and j['error']['error_subcode'] == 1545041:
				# user has quit chat, delete them
				print 'User', ids[i], 'quit Floc'
				db.query("DELETE FROM users where id="+str(ids[i]))
			else:
				print "ERROR:", str(j)
		i+=1

##

def save_message(identity,msg):
	db.insert('messages',time=msg['timestamp'],data=json.dumps({'identity':identity,'msg':msg['message']}))

##### MSG FUNCTION

def Chat_msg(sess,msg):
	# check not spam
	timedff = msg['timestamp'] - sess.last_sent
	if timedff < 200:# 0.2 seconds
		print 'timedff', timedff, 'SPAM', TESTING
		if TESTING is False:
			return False
	elif timedff > 420000:# 7 mins
		sess = set_identity(sess)

	# Special Cases
	if 'text' in msg['message']:
		r = check_text(sess,msg['message']['text'])
		if type(r) == str:
			return sess, r
		r = special_cases(sess,msg['message']['text'])
		if r is not False:
			return r
	# manage attachments
	if 'attachments' in msg['message'] and (msg['message']['attachments'][0]['payload'] is None or 'sticker_id' in msg['message']['attachments'][0]['payload'] or msg['message']['attachments'][0]['type'] not in ['video', 'image']):
		if 'text' not in msg['message']:
			return sess, 'Not sent.\nCan only send videos and images.'
		else:
			del msg['message']['attachments']
	# save message
	save_message(sess.identity,msg)
	# Send Message
	sess = group_msg(sess,msg['message'])
	sess.update(last_sent=msg['timestamp'])
