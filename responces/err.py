# -*- coding: utf-8 -*-

import bot
from chat import Chat_msg

ErrLen_start = "🐧 Not Sent\nMust be under 200 characters."
def ErrLen_msg(sess,msg):
	# filter msg
	if 'text' in msg:
		try:
			msg['text'] = textfilter(msg['text'])
		except Exception as e:
			if str(e) == 'ErrLen':
				return "🐧 Still too long.\nTry removing emojis."
	# send to regular chat
	bot.setmsg(sess,'Chat')
	return Chat_msg(msg)


ErrNewlines_start = "🐧 Not Sent\nMust have less than 5 newline characters."
def ErrNewlines_msg(sess,msg):
	# filter msg
	if 'text' in msg:
		try:
			msg['text'] = textfilter(msg['text'])
		except Exception as e:
			if str(e) == 'ErrNewlines':
				return "🐧 Still too long.\nTry removing emojis."
	# send to regular chat
	bot.setmsg(sess,'Chat')
	return Chat_msg(msg)


ErrSticker_start = "🐧 Not Sent\nI can't send stickers😢."
def ErrSticker_msg(sess,msg):
	# filter msg
	if msg == 'Err:sticker':
		return "🐧 That is still a sticker.\nWhy not send a GIF instead?"
	# send to regular chat
	bot.setmsg(sess,'Chat')
	return Chat_msg(msg)
