# -*- coding: utf-8 -*-
import web, time
import testbot
from emojis import emojis

testbot.send_to = 'http://0.0.0.0:8080/webhook'
db = web.database(dbn='postgres',db='secret',user='postgres',pw='',host='localhost')

userI = 1

def run():
	'''
	clear_tables()
	addgroups()
	#
	new_user()
	#
	'''
	clear_tables()
	addgroups()
	#
	temp_messages(get_users(4))
	#
	base_groups(get_users(1)[0])
	#
	message_groups(get_users(4))
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
	db.query("delete from groups")
	db.query("delete from group_users")
	db.query("delete from temp_groups")
	testbot.clear_messages()

def addgroups():
	db.query("""
		INSERT INTO groups (name,location)
		VALUES
			('cs2',point(-85.0,0.0)),
			('indieHackers',point(-85.0,0.0)),
			('maths2',point(-85.00351351351,0.00351351351))
	""")

def get_users(amount):
	global userI
	users = []
	for id in range(amount+userI)[userI:]:
		u = testbot.User(id)
		u.postback("GetStarted")
		u.sendlocation()
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
		"Welcome to Floc.\nFloc lets you chat anonymously with people around you.",
		"First we need your location so we can see who's nearby."
	)
	user.sendlocation()
	user.did_receive("Done!\nYou can join chat groups from the #Groups below and chat with people nearby.", suggest=['#cs2','#indieHackers','#maths2'])

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

# Temp Groups

def temp_messages(users):
	users[0].send('Hello')
	users[0].send('How is everyone?')
	iden0 = identity(users[0].id)
	users[1].did_receive(emojis[iden0]+' Hello', emojis[iden0]+' How is everyone?')
	users[1].send('Im good')
	iden1 = identity(users[1].id)
	users[0].did_receive(emojis[iden1]+' Im good')
	users[2].did_receive(emojis[iden0]+' Hello', emojis[iden0]+' How is everyone?', emojis[iden1]+' Im good')

# Messaging Groups

def message_groups(users):
	group_id = str(db.query("SELECT id from groups where name='maths2'")[0]['id'])
	users[0].quick_reply('#maths2')
	users[1].quick_reply('#maths2')
	users[2].quick_reply('#maths2')
	send_recieve_groups(group_id,users)
	reset_identity_groups(group_id,users)

def reset_identity_groups(group_id,users):
	return False

	# get curr identity
	idenOld = identity(users[0].id)
	# set the time offset
	users[0].time_offset = 10
	# send message
	users[0].send('Test')
	# check for new identity in message
	time.sleep(0.5)
	idenNew = identity(users[0].id)
	testbot.addresult([idenOld == idenNew,'not '+str(idenOld),str(idenNew)])
	users[1].did_receive(emojis[idenNew]+' Test')

def send_recieve_groups(group_id,users):
	users[0].send('Hello')
	users[0].send('How is everyone?')
	iden0 = identity(users[0].id)
	users[1].did_receive(emojis[iden0]+' Hello', emojis[iden0]+' How is everyone?')
	users[1].send('Im good')
	iden1 = identity(users[1].id)
	users[0].did_receive(emojis[iden1]+' Im good')
	users[2].did_receive(emojis[iden0]+' Hello', emojis[iden0]+' How is everyone?', emojis[iden1]+' Im good')

# Making/Join/Leave Groups

def base_groups(user):
	makeleave_group(user)
	joinleave_group(user)

def joinleave_group(user):
	user.quick_reply('#cs2')
	user.did_receive("Joined #cs2", suggest=['<','pin #cs2'])
	user.quick_reply('<')
	user.did_receive("Left group")

def makeleave_group(user):
	user.send('#frisbae')
	user.did_receive("Make group #frisbae?", suggest=['Yes','No'])
	user.quick_reply('Yes')
	user.did_receive("Joined #frisbae", suggest=['<','pin #frisbae'])
	user.quick_reply('<')
	user.did_receive("Left group")

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
