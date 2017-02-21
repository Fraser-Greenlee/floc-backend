
import web, sys, random
import bot

urls = (
		'/webhook', 'webhook',
		'/(.*)', 'empty'
)
app = web.application(urls, globals())

# define Session vars
session = bot.Session(id=None, current_msg='Start', last_msg_tstamp=0, identity=random.randint(0,241))

class webhook:
	def GET(self):
		return bot.verify(web.input())
	def POST(self):
		print web.data()
		r = bot.recieve(web.data(), session)
		sys.stdout.flush()
		return r

class empty:
	def GET(self, name):
		return 'nothing to see here'

if __name__ == "__main__":
	app.run()
