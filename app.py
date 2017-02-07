# -*- coding: utf-8 -*-
import web
import bot
import sys

urls = (
		'/webhook', 'webhook',
		'/(.*)', 'empty'
)
app = web.application(urls, globals())

class webhook:
	def GET(self):
		return bot.verify(web.input())
	def POST(self):
		# show request data
		print web.data()
		sys.stdout.flush()
		#
		return bot.recieve(web.data())

class empty:
	def GET(self, name):
		return 'nothing to see here'

if __name__ == "__main__":
		app.run()
