import web
import bot

import os
import sys
print "DATABASE_URL"
print os.environ.get('DATABASE_URL')
sys.stdout.flush()

urls = (
		'/webhook', 'webhook',
		'/(.*)', 'empty'
)
app = web.application(urls, globals())

class webhook:
	def GET(self):
		return bot.verify(web.input())
	def POST(self):
		return bot.recieve(web.data())

class empty:
	def GET(self, name):
		return 'nothing to see here'

if __name__ == "__main__":
		app.run()
