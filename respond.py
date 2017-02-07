# -*- coding: utf-8 -*-
import bot
from tokens import db

def txt(msg):
	return {'text':unicode(msg, 'utf-8')}

class Start:
	@staticmethod
	def recieve(id,message):
		bot.send(
			id,
			txt("🐧 Welcome to Secret.\nA place for anonymous group chats on Messenger.")
		)
		bot.setmessage(id,'chat')

#################

def textfilter(text):
	if len(text) > 200:
		raise Exception('ErrLen')
	if len(text.split('\n'))-1 >= 5:
		raise Exception('ErrNewlines')
	return text

def fromMsg(raw_message):
	message = {}
	if 'text' in raw_message:
		message['text'] = raw_message['text']
	if 'attachments' in raw_message:
		message['attachment'] = raw_message['attachments'][0]
		if 'sticker_id' in raw_message['attachments'][0]['payload']:
			return 'Err:sticker'
	#
	return message
#


class Chat:
	@staticmethod
	def start(id):
		return False

	@staticmethod
	def recieve(id,message):
		## filter message
		# catch Err's
		message = fromMsg(message)
		if message == 'Err:sticker':
			bot.setmessage(id,'ErrSticker')
			return False
		if 'text' in message:
			try:
				message['text'] = textfilter(message['text'])
			except Exception as e:
				if str(e) == 'ErrLen':
					bot.setmessage(id,'ErrLen')
					return False
				elif str(e) == 'ErrNewlines':
					bot.setmessage(id,'ErrNewlines')
					return False
		## send message
		q = db.query("SELECT id FROM users WHERE id<>"+str(id))
		# send to all ids
		return False

'''
for r in q:
	id = r['id']
	try:
		bot.send(
			id,
			message
		)
	except bot.SendError as e:
		print "code:", e.code
		if e.code == 200:
			# user has left, delete user from database
			db.query("DELETE FROM users WHERE id="+str(id))
		else:
			# proper error
			print "ERROR:", e.jsn
'''
a = 3

#


################ Error messages

class ErrLen:
	@staticmethod
	def start(id):
		bot.send(
			id,
			txt("🐧 Not Sent\nMust be under 200 characters.")
		)

	@staticmethod
	def recieve(id,message):
		# filter message
		if 'text' in message:
			try:
				message['text'] = textfilter(message['text'])
			except Exception as e:
				if str(e) == 'ErrLen':
					bot.send(
						id,
						txt("🐧 Still too long.\nTry removing emojis.")
					)
					return False
		# send to regular chat
		bot.setmessage(id,'chat')
		Chat.recieve(id, message)


class ErrNewlines:
	@staticmethod
	def start(id):
		bot.send(
			id,
			txt("🐧 Not Sent\nMust have less than 5 newline characters.")
		)

	@staticmethod
	def recieve(id,message):
		# filter message
		if 'text' in message:
			try:
				message['text'] = textfilter(message['text'])
			except Exception as e:
				if str(e) == 'ErrNewlines':
					bot.send(
						id,
						txt("🐧 Still too long.\nTry removing emojis.")
					)
					return False
		# send to regular chat
		bot.setmessage(id,'chat')
		Chat.recieve(id, message)


class ErrSticker:
	@staticmethod
	def start(id):
		bot.send(
			id,
			txt("🐧 Not Sent\nI can't send stickers😢.")
		)

	@staticmethod
	def recieve(id,message):
		# filter message
		if message == 'Err:sticker':
			bot.send(
				id,
				txt("🐧 That is still a sticker.\nWhy not send a GIF instead?")
			)
			return False
		# send to regular chat
		bot.setmessage(id,'chat')
		Chat.recieve(id, message)
