# -*- coding: utf-8 -*-
from chat import Chat_msg
from err import *#ErrLen_start, ErrLen_msg, ErrSticker_start, ErrSticker_msg, ErrNewlines_start, ErrNewlines_msg

def Start_msg(sess, msg):
		bot.setmsg(sess,'Chat')
		return "🐧 Welcome to Secret.\nA place for anonymous group chats on Messenger."
