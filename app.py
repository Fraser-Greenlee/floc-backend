import web
import bot

urls = (
		'/webhook', 'webhook',
		'/(.*)', 'empty'
)
app = web.application(urls, globals())
#db = web.database(dbn='postgres', db='d8bqtbsqkdmogn', user='tatvwdylfhnthu', pw='9aa3223d040c65ef06e9362022004fe9bb5b3e3f44b67ad4101f549fddaa8177', host='ec2-54-204-1-40.compute-1.amazonaws.com')

class webhook:
	def GET(self):
		return bot.verify(web.input())
	def POST(self):
		id = bot.messagedata(web.data())['id']
		bot.send(id, "test")
		#return bot.recieve(web.data(), db)

class empty:
	def GET(self, name):
		return 'nothing to see here'

if __name__ == "__main__":
		app.run()
