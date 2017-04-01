# -*- coding: utf-8 -*-
import bot, json, time
from chat import Chat_msg, set_identity, group_msg
from quick_replies import *
from tokens import db
from emojis import emojis

def Start_msg(sess, msg):
	bot.send(sess.id, "Welcome to Floc.\nFloc lets you chat anonymously with people around you.")
	time.sleep(1)
	# send last 30 messages
	send_last_messages(sess.id)
	# set user's identity
	sess = set_identity(sess)
	group_msg(sess, "Joined")
	sess.update(current_msg='Chat')


def send_last_messages(id):
	print 'last messages'
	q = db.query("SELECT time from messages order by time desc limit 30")
	if len(q) == 0:
		return False
	min_time = q[len(q)-1]['time']
	msgs = []
	for r in db.query("SELECT data from messages where time >= "+str(min_time)+" order by time asc"):
		msgs += make_messages(id,r['data']['identity'], r['data']['msg'])
	bot.send(id,*msgs)

def make_messages(id,identity,msg):
	if type(msg) == str:
		msg = unicode(msg,'utf-8')
	if type(msg) == unicode:
		msg = {u'text':msg}
	#
	if 'mid' in msg and 'seq' in msg:
		del msg['mid']
		del msg['seq']
	#
	if 'attachments' in msg:
		msg['attachment'] = msg['attachments'][0]
		del msg['attachments']
		if 'text' in msg:
			nmsg = dict(msg)
			del nmsg['text']
			return [emojis[identity]+u' '+unicode(msg['text'])]
		else:
			return [emojis[identity], msg]
	else:
		return [emojis[identity]+u' '+unicode(msg['text'])]
