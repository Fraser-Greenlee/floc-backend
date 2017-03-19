# -*- coding: utf-8 -*-
import bot
from chat import Chat_msg, select_group, joinmake_temp_group, mid_to_tstamp
from quick_replies import *

def Start_msg(sess, msg):
	bot.send(sess.id, "Welcome to Floc.\nFloc lets you chat anonymously with people around you.")
	bot.send(sess.id, "First we need your location so we can see who's nearby.", suggest='$location')
	bot.setmsg(sess, 'Location')

def Location_msg(sess, msg):
	if 'attachments' not in msg or 'coordinates' not in msg['attachments'][0]['payload']:
		bot.send(sess.id, "We need your location so we can see who's nearby.", suggest='$location')
		return False
	sess.update(current_msg='Chat')
	# save location
	coords = msg['attachments'][0]['payload']['coordinates']
	# Take Longitude/2 so scales equally to lattitude
	sess.update(location='$point('+str([coords['lat'],coords['long']/2])[1:-1]+')')# $ to stop quotes round str value
	sess.set(lat=coords['lat'],long=coords['long']/2)
	# set to chat
	sug = select_group(sess)
	if sug != False:
		sess.update(quick_replies=str(sug).replace("'","''"))
		bot.send(sess.id, "Done!\nYou can join chat groups from the #Groups below and chat with people nearby.", suggest=sug)
	else:
		bot.send(sess.id, "Done!\nYou can make chat groups by entering '#my-group-name' below and chat with people nearby.", suggest=sug)
	joinmake_temp_group(sess, mid_to_tstamp(msg['mid']))
