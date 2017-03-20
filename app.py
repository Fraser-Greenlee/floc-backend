
import web, sys
import bot

urls = (
		'/webhook', 'webhook',
		'/(.*)', 'empty'
)
app = web.application(urls, globals())

class webhook:
	def GET(self):
		return bot.verify(web.input())
	def POST(self):
		session = bot.Session(id=None, current_msg='Start', location=0, lat=0, long=0, open_group=0, recieve_messages=True, temp_group_id=0, group_name='', last_sent=0, identity=0, quick_replies='')
		print web.data()
		r = bot.recieve(web.data(), session)
		sys.stdout.flush()
		return r

class empty:
	def GET(self, name):
		return open('webpage/index.html','r').read()

if __name__ == "__main__":
	app.run()
