# -*- coding: utf-8 -*-

import bot
from chat import Chat_msg, textfilter

def errorfilter(sess,msg,error_from,rep_error_msg):
	if 'text' in msg:
		msg['text'] = textfilter(msg['text'])
		if type(msg['text']) == list:
			error = msg['text'][0]
			if error == error_from:
				return rep_error_msg
			else:
				return bot.setmsg(sess, error)
	return False

#


ErrLen_start = "🐧 Not Sent\nMust be under 200 characters."
def ErrLen_msg(sess,msg):
	# filter msg
	r = errorfilter(sess,msg,'ErrLen',"🐧 Still too long.\nTry removing emojis.")
	if r is not False:
		return r
	# send to regular chat
	bot.setmsg(sess,'Chat')
	return Chat_msg(sess,msg)


ErrNewlines_start = "🐧 Not Sent\nMust have less than 5 newline characters."
def ErrNewlines_msg(sess,msg):
	# filter msg
	r = errorfilter(sess,msg,'ErrNewlines',"🐧 Still too many.")
	if r is not False:
		return r
	# send to regular chat
	bot.setmsg(sess,'Chat')
	return Chat_msg(sess,msg)


ErrSticker_start = "🐧 Not Sent\nI can't send stickers😢."
def ErrSticker_msg(sess,msg):
	# filter msg
	if msg == 'Err:sticker':
		return "🐧 That is still a sticker.\nWhy not send a GIF instead?"
	# send to regular chat
	bot.setmsg(sess,'Chat')
	return Chat_msg(sess,msg)
