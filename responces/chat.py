# -*- coding: utf-8 -*-
from datetime import datetime
import bot, random, re, web
from emojis import emojis
from tokens import db, TESTING, LOCAL_TEST

##### FUNCTIONS

def mid_to_tstamp(mid):#mid = "mid.1486498717604:38098ec617"
	return int(mid[4:mid.index(':')])

## Status Bar

def select_group(sess):
	# Select groups within ~1.5km radius. 1 + 0.025056848879657423
	user_groups = []
	user_q = [r for r in
		db.query("""
			SELECT
				id, name
			FROM
				groups
			WHERE
				location <@ circle '(({x},{y}), 1.025056848879657423)'
		""".format(x=sess.lat,y=sess.long) )
	]
	if len(user_q) == 0:
		return False
	groups = [
		[
			'#'+group['name'],
			"open_group:"+group['name']+":"+str(group['id'])
		]
		for group in user_q
	]
	return groups

#### Handle Special Actions

def active(sess):
	if sess.open_group != 0:
		return u''.join([emojis[r['identity']] for r in db.query("SELECT identity from users where open_group="+str(sess.open_group)+" and id<>"+str(sess.id))])
	elif sess.temp_group_id:
		return u''.join([emojis[r['identity']] for r in db.query("SELECT identity from users where temp_group_id="+str(sess.temp_group_id)+" and id<>"+str(sess.id))])

def reset(sess):
	if sess.open_group != 0:
		sess = set_group_identity(sess)
		group_msg(sess, 'Joined')
	else:
		sess = set_temp_identity(sess)
	return [u'You are now '+emojis[sess.identity], sess]

def me(sess):
	return u'You are '+emojis[sess.identity]

def special_cases(sess,text):
	if sess.open_group == 0 and text[0] == '#':
		ret = find_group(sess,text[1:])
	elif text[0] == '@':
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

## Handle Groups

def in_group_suggestions(name,group_id):
	return [['leave #'+name,'leave_group']]

def find_group(sess,name):
	finder = re.compile('[^0-9a-zA-Z-]')#chars, numbers and dash
	if len(finder.findall(name)) > 0:
		return 'Group names can only contain letters, numbers and - characters.'
	#
	q = db.query("""
		SELECT id
		from groups
		where name='{name}' and location <@ circle '(({x}, {y}),0.025056848879657423)'
	""".format(name=name,x=sess.lat,y=sess.long))
	if len(q) > 0:
		# should never be more than one same name within radius
		return open_group(sess, q[0]['id'], name)
	else:
		return make_group(sess, name)

def make_group(sess,name):
	sess.update(recieve_messages=False)
	bot.send(sess.id, u"Make group #"+name+u"?", suggest=[['Yes','make_group_actually:'+name],['No','dont_make_group']])

def set_group_identity(sess):
	sess.update(identity=db.query("""
		SELECT s
		FROM generate_series(1, 241) s
		WHERE s NOT IN (SELECT identity FROM users WHERE open_group={group_id})
		order by s asc limit 1
	""".format(group_id=sess.open_group))[0]['s'])
	return sess

def set_temp_identity(sess):
	sess.update(identity=db.query("""
		SELECT s
		FROM generate_series(1, 241) s
		WHERE s NOT IN (SELECT identity FROM users WHERE open_group=0 and temp_group_id={temp_group_id})
		order by s asc limit 1
	""".format(temp_group_id=sess.temp_group_id))[0]['s'])
	return sess

def joinmake_temp_group(sess,temp_last_active):
	q = db.query("""
		SELECT
			id,
			|/ (({x} - location[0])^2 + ({y} - location[1])^2) as distance
		FROM
			temp_groups
		WHERE
			location <@ circle '(({x},{y}),1.00026483786529496456)'
		order by distance asc
	""".format(x=sess.lat,y=sess.long))
	if len(q) > 0:
		group_id = q[0]['id']
	else:
		# make group
		group_id = db.insert('temp_groups',location=web.SQLLiteral('point('+str(sess.lat)+','+str(sess.long)+')'))
	# join group
	sess.update(temp_group_id=group_id,last_sent=temp_last_active)
	sess = set_temp_identity(sess)
	temp_group_msg(sess, "Joined")
	return sess

##

def group_msg(sess,msg):
	print 'GROUP MSG', msg
	if type(msg) == str:
		msg = unicode(msg,'utf-8')
	if type(msg) == unicode:
		msg = {u'text':msg}
	elif 'mid' in msg and 'seq' in msg:
		del msg['mid']
		del msg['seq']
	idlist =  [r['id'] for r in db.query("SELECT id FROM users WHERE recieve_messages=true and open_group="+str(sess.open_group)+" AND id<>"+str(sess.id))]
	s = in_group_suggestions(sess.group_name,sess.open_group)
	if 'attachments' in msg:
		errors = bot.send(idlist, emojis[sess.identity], msg, suggest=s)
	else:
		errors = bot.send(idlist, emojis[sess.identity]+u' '+unicode(msg['text']), suggest=s)
	if LOCAL_TEST:
		for err in errors:
			if err['code'] == 200:
				print 'ERROR: user has deleted?'
			else:
				print "ERROR:", str(err)
	return sess

def temp_group_msg(sess,msg):
	if LOCAL_TEST:
		print 'TEMP GROUP MSG', msg
	if type(msg) == str:
		msg = unicode(msg,'utf-8')
	if type(msg) == unicode:
		msg = {u'text':msg}
	ids = []
	suggests = []
	for r in db.query("SELECT id, quick_replies FROM users WHERE recieve_messages=true and open_group=0 and temp_group_id="+str(sess.temp_group_id)+" AND id<>"+str(sess.id)):
		ids.append(r['id'])
		suggests.append(r['quick_replies'])
	#
	if 'attachments' in msg:
		errors = bot.send(ids, emojis[sess.identity], msg, suggests=suggests)
	else:
		errors = bot.send(ids, emojis[sess.identity]+u' '+unicode(msg['text']), suggests=suggests)
	if LOCAL_TEST:
		for err in errors:
			if err['code'] == 200:
				print 'ERROR: user has deleted?'
			else:
				print "ERROR:", str(err)
	return sess

##### MSG FUNCTION

def Chat_msg(sess,msg):
	#
	# TODO Check for message error
	#
	timedff = mid_to_tstamp(msg['mid']) - sess.last_sent
	if timedff < 200:
		print 'SPAM'
		if TESTING:
			return False

	# Set group
	in_temp = sess.open_group == 0
	if in_temp:
		if sess.temp_group_id == 0 or timedff > 600000:
			sess = joinmake_temp_group(sess,mid_to_tstamp(msg['mid']))
		sess.status_bar = select_group(sess)
	else:
		if timedff > 600000:
			set_group_identity(sess)
		sess.status_bar = in_group_suggestions(sess.group_name, sess.open_group)
	# Special Cases
	if 'text' in msg:
		r = check_text(sess,msg['text'])
		if type(r) == str:
			return sess, r
		r = special_cases(sess,msg['text'])
		if r is not False:
			return r
	elif 'attachments' in msg and 'sticker_id' in msg['attachments'][0]['payload']:
		return sess, 'Not sent.\nCannot send stickers.'
	# Send Message
	if in_temp:
		sess = temp_group_msg(sess,msg)
	else:
		sess = group_msg(sess,msg)
	bot.send(sess.id,"Sent",suggest=sess.status_bar)
