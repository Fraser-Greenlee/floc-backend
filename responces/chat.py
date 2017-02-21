from datetime import datetime
from dateutil.tz import tzlocal
import bot, random
from emojis import emojis
from tokens import db


##### TOOLS


def textfilter(text):
	if len(text) > 200:
		return ['ErrLen']
	if len(text.split('\n'))-1 >= 5:
		return ['ErrNewlines']
	return text


##### FUNCTIONS


def from_msg(sess,raw_message):
	# add emoji and stop stickers
	message = {}
	if 'text' in raw_message:
		message['text'] = unicode(emojis[sess.identity], 'utf-8')+' '+raw_message['text']
	if 'attachments' in raw_message:
		message['attachment'] = raw_message['attachments'][0]
		if 'sticker_id' in raw_message['attachments'][0]['payload']:
			return ['Err:sticker']
	return message


def mid_to_tstamp(mid):#mid = "mid.1486498717604:38098ec617"
	return int(mid[4:mid.index(':')])


def emoji_spam(sess,msg):
	dff = mid_to_tstamp(msg['mid']) - sess.last_msg_tstamp
	if dff < 200:# is spam
		return False
	elif dff > 600000:
		# off for over 10mins, reset emoji
		# set to a random unused value
		sess.set(
			identity=db.query("""
				with new_identity as (
				SELECT s
					FROM generate_series(1, 241) s
					LEFT JOIN users ON s.s = identity
				 WHERE id IS NULL
				 order by random() limit 1
				)
				UPDATE users SET identity=new_identity.s
				FROM new_identity
				WHERE id=1166543533459050;
				select identity from users where id=1166543533459050
				""")[0]['identity']
		)
	return sess


def catch_errors(sess, msg):
	if msg == ['Err:sticker']:
		return ['ErrSticker']
	if 'text' in msg:
		r = textfilter(msg['text'])
		if type(r) == list:
			if r == ['ErrLen']:
				return ['ErrLen']
			elif r == ['ErrNewlines']:
				return ['ErrNewlines']
		msg['text'] = r
	return msg


def save_msg(sess,msg):
	d = {'tstamp':mid_to_tstamp(msg['mid']), 'text':'', 'type':'', 'data':'', 'uid':sess.id}
	if 'text' in msg:
		d['text'] = msg['text']
	if 'attachments' in msg:
		d['type'] = msg['attachments'][0]['type']
		d['data'] = msg['attachments'][0]['payload']['url']
	db.insert('messages',tstamp=d['tstamp'],text=d['text'],type=d['type'],data=d['data'],uid=d['uid'])


def send_msg(sess,msg):
	q = db.query("SELECT id FROM users WHERE id<>"+str(sess.id))
	idlist = [r['id'] for r in q]
	if 'attachment' in msg:
		# send emoji before each attachment
		errors = bot.send(idlist, emojis[sess.identity]) + bot.send(idlist, msg)
	else:
		errors = bot.send(idlist, msg)
	for err in errors:
		print err
		if err['code'] == 200:
			# user has left, delete user from database
			db.query("DELETE FROM users WHERE id="+str(sess.id))
		else:
			# proper error
			print "ERROR:", err.jsn


##### MSG FUNCTION


def Chat_msg(sess,msg):
	# set emoji and stop spam
	sess = emoji_spam(sess, msg)
	if sess is False:
		return False
	db.query("UPDATE users SET last_msg_tstamp="+str(mid_to_tstamp(msg['mid']))+" WHERE id="+str(sess.id))
	# filter content
	new_msg = from_msg(sess,msg)
	new_msg = catch_errors(sess,new_msg)
	if type(new_msg) == list:
		return bot.setmsg(sess,new_msg[0])
	# save message
	save_msg(sess,msg)
	# send message to all other ids
	send_msg(sess,new_msg)
