
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
		# show request data
		print web.data()
		sys.stdout.flush()
		#
		return bot.recieve(web.data(), session)

class empty:
	def GET(self, name):
		return 'nothing to see here'

if __name__ == "__main__":
		app.run()
