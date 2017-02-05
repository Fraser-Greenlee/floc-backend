# -*- coding: utf-8 -*-
import bot
from tokens import db


class Start:
	@staticmethod
	def start(id):
		return False

	@staticmethod
	def recieve(id,message):
		bot.send(
			id,
			"""Welcome to Secret.\nA place for anonymous group chats on Messenger."""
		)
		bot.setmessage(id,'chat')


def textfilter(text):
	if len(text) > 200:
		raise Exception('ErrLen')
	if len(text.split('\n'))-1 >= 5:
		raise Exception('ErrNewlines')
	return text

class Chat:
	@staticmethod
	def start(id):
		return False

	@staticmethod
	def recieve(id,message):
		## filter message
		# catch Err's
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
		idlist = []
		for r in q:
			idlist.append(r['id'])
		# send to all ids in list
		bot.send(
			idlist,
			message
		)


################ Error messages

def errtxt(string):
	return {'text':unicode(string, 'utf-8')}


class ErrLen:
	@staticmethod
	def start(id):
		bot.send(
			id,
			errtxt("🐙 Not Sent\nMust be under 200 characters.")
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
						errtxt("🐙 Still too long.\nTry removing emojis.")
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
			errtxt("🐙 Not Sent\nMust have less than 5 newline characters.")
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
						errtxt("🐙 Still too long.\nTry removing emojis.")
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
			errtxt("🐙 Not Sent\nI can't send stickers😢.")
		)

	@staticmethod
	def recieve(id,message):
		# filter message
		if message == 'Err:sticker':
			bot.send(
				id,
				errtxt("🐙 That is still a sticker.\nWhy not send a GIF instead?")
			)
			return False
		# send to regular chat
		bot.setmessage(id,'chat')
		Chat.recieve(id, message)
