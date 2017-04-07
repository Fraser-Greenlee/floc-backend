# -*- coding: utf-8 -*-
import web, time
import testbot
from emojis import emojis

testbot.send_to = 'http://0.0.0.0:5000/webhook'
db = web.database(dbn='postgres',db='secret',user='postgres',pw='',host='localhost')

userI = 1

def run():
	clear_tables()
	#
	new_user()
	#
	old_msgs()
	#
	actions(get_users(1)[0])
	#
	errors(get_users(1)[0])
	#
	testbot.results()
	clear_tables()

## Tools

def clear_tables():
	global userI
	userI = 1
	db.query("delete from users")
	db.query("delete from messages")
	testbot.clear_messages()


def get_users(amount):
	global userI
	users = []
	for id in range(amount+userI)[userI:]:
		u = testbot.User(id)
		u.postback("GetStarted")
		users.append(u)
	userI += amount
	return users

def last_msg(user,equals):
	try:
			l = user.last_msg()['message']['text']
			testbot.equals( l[l.index(' ')+1:] , equals)
	except:
		print 'WARNING: last_msg does not have text'
		testbot.equals( "$Error: non text message." , equals)

def identity(id):
	return db.query("SELECT identity from users where id="+str(id))[0]['identity']

## Test Cases

def new_user():
	user = testbot.User()
	user.postback("GetStarted")
	user.did_receive(
		"Welcome to Floc.\nFloc lets you chat anonymously with people around you.")

#

def old_msgs():
	user = testbot.User()
	user.postback("GetStarted")
	listener = testbot.User()
	listener.postback("GetStarted")
	for i in range(31):
		user.send(str(i))
	#
	new_user = testbot.User()
	new_user.postback("GetStarted")
	new_user.did_receive(* [str(i) for i in range(30)[1:]]+["Welcome to Floc.\nFloc lets you chat anonymously with people around you."])

# Errors

def errors(user):
	user.send('a'*201)
	user.did_receive('Not sent.\nMessage must be under 200 characters.')
	user.send('a\n'*6)
	user.did_receive('Not sent.\nMessage has too many new lines.')

# Actions

def actions(user):
	user.send('@bla')
	user.did_receive('Not an action\nTo see all actions send "@actions"')
	user.send('@actions')
	user.did_receive('@active, see active users\n@reset, reset your emoji\n@me, see your current emoji')
	user.send('@me')
	oldIdentity = identity(user.id)
	user.did_receive('You are '+emojis[oldIdentity])
	user.send('@reset')
	time.sleep(1)
	newIdentity = identity(user.id)
	user.did_receive('You are now '+emojis[newIdentity])
	user.send('@active')

# error checking

def error_handles(users):
	r = []
	r += err_len(users)
	r += err_newlines(users)
	return r

def err_len(user0,user1):
	user0.send("a"*201)
	user0.did_receive("Not Sent\nMust be under 200 characters.")
	user0.send("a"*201)
	user0.did_receive("Still too long.\nTry removing emojis.")
	user0.send("x")
	last_msg(user1, "x")
	return r

def err_newlines(user0,user1):
	user0.send('\n'*5)
	user0.did_receive("Not Sent\nMust have less than 5 newline characters.")
	user0.send('\n'*5)
	user0.did_receive("Still too many.")
	user0.send("x")
	last_msg(user1, "x")
	return r
