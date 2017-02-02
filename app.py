import web
import bot
import tokens

# for testing
key = tokens.test

urls = (
		'/webhook', 'webhook',
		'/(.*)', 'empty'
)
app = web.application(urls, globals())
db = web.database(dbn='postgres', db='detehdd6fac66k', user='ajgessvxsdughz', pw='ff89f60c9833762748cb7325758b4d65b2e48bff957bc30431441287e19d71c2', host='ec2-54-221-255-153.compute-1.amazonaws.com')

class webhook:
	def GET(self):
		return bot.verify(web.input(), key)
	def POST(self):
		return bot.recieve(web.data(), db)

class empty:
	def GET(self, name):
		return 'nothing to see here'

if __name__ == "__main__":
		app.run()
