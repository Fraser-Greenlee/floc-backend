# -*- coding: utf-8 -*-
import web
import testbot

testbot.send_to = 'http://0.0.0.0:8080/webhook'
db = web.database(dbn='postgres',db='secret',user='postgres',pw='',host='localhost')

def run():
	results = []
	clear_tables()
	#
	results.append(new_user())
	clear_tables()
	#
	users = get_users()
	results.append(new_identity(users))
	clear_tables()
	#
	users = get_users()
	#
	results += send_msg(users)
	results += error_handles(users)
	#
	testbot.results(results)
	clear_tables()

## Tools

def clear_tables():
	db.query("delete from users")
	db.query("delete from messages")
	testbot.clear_messages()

def get_users():
	users = []
	for id in [1,2,3,4,5]:
		u = testbot.User(id)
		u.postback("GetStarted")
		users.append(u)
	return users

def last_msg(user,equals):
	try:
			l = user.last_msg()['message']['text']
			return testbot.equals( l[l.index(' ')+1:] , equals)
	except:
		print 'WARNING: last_msg does not have text'
		return testbot.equals( "$Error: non text message." , equals)

## Test Cases

def new_user():
	user = testbot.User()
	user.postback("GetStarted")
	return user.did_receive("🐧 Welcome to Floc.\nA place for anonymous group chats on Messenger.")

# Updating identity

def new_identity(users):
	users[0].send('x')
	l = users[1].last_msg()['message']['text']
	current_emoji = l[:l.index(' ')]
	#
	users[0].time_offset = 600001
	users[0].send('x')
	l = users[1].last_msg()['message']['text']
	new_emoji = l[:l.index(' ')]
	return testbot.test(current_emoji != new_emoji, "Emoji changes", "No emoji change.")

# sending messages

def send_msg(users):
	r = []
	r.append(text_to_all(users[1:],"x"))
	r.append(attachment_to_all(users[1:],{'type':"image",'payload':{'url':'http://blahblah.com'}}))
	return r

def text_to_all(users,msg):
	users[0].send(msg)
	r = []
	for u in users[1:]:
		r.append(last_msg(u, msg))
	fl = [v[0] for v in r]
	if False in fl:
		return r[fl.index(False)]
	return testbot.test(True,'Send to all "x"','')

def attachment_to_all(users,attachment):
	users[0].send(attachment)
	r = []
	for u in users[1:]:
		r.append(u.did_receive(attachment))
	fl = [v[0] for v in r]
	if False in fl:
		return r[fl.index(False)]
	return testbot.test(True,'Send to all "'+str(attachment)+'"','')

# error checking

def error_handles(users):
	r = []
	r += err_len(users)
	r += err_newlines(users)
	return r

def err_len(users):
	r = []
	users[0].send("a"*201)
	r.append(users[0].did_receive("🐧 Not Sent\nMust be under 200 characters."))
	users[0].send("a"*201)
	r.append(users[0].did_receive("🐧 Still too long.\nTry removing emojis."))
	users[0].send("x")
	r.append(last_msg(users[1], "x"))
	return r

def err_newlines(users):
	r = []
	users[0].send('\n'*5)
	r.append(users[0].did_receive("🐧 Not Sent\nMust have less than 5 newline characters."))
	users[0].send('\n'*5)
	r.append(users[0].did_receive("🐧 Still too many."))
	users[0].send("x")
	r.append(last_msg(users[1], "x"))
	return r
