# -*- coding: utf-8 -*-
import web, bot
from tokens import db
from chat import set_group_identity, in_group_suggestions, select_group, group_msg

def make_group_actually(sess,name):
	name = name[0]
	group_id = db.insert('groups', name=name, location=web.SQLLiteral('point('+str(sess.lat)+','+str(sess.long)+')'))
	sess.update(recieve_messages=True)
	open_group(sess,[name,group_id])

def dont_make_group(sess):
	sess.update(recieve_messages=True)
	bot.send(sess.id, u"Canceled", suggest=select_group(sess))

def leave_group(sess):
	sess.update(open_group=0)
	bot.send(sess.id, u"Left group", suggest=select_group(sess))

def open_group(sess,namegroup_id):
	name, group_id = namegroup_id
	if db.query("SELECT count(*) from group_users where user_id="+str(sess.id)+" and group_id="+str(group_id))[0]['count'] == 0:
		db.insert('group_users',group_id=group_id,user_id=sess.id)
	sess.update(open_group=group_id,group_name=str(name),temp_group_id=0)
	sess = set_group_identity(sess)
	status_bar = in_group_suggestions(name,group_id)
	group_msg(sess,u'Joined')
	bot.send(sess.id, u'Joined #'+name, suggest=status_bar)
