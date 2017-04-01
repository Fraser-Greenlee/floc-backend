import bot
from flask import Flask, request, abort, send_from_directory
import os.path

app = Flask(__name__)


@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
	if request.method == 'GET':
		return bot.verify(request)
	elif request.method == 'POST':
		session = bot.Session(id=None, current_msg='Start', recieve_messages=True, last_sent=0, last_recieved=0, last_read=0, identity=0)
		bot.recieve(request.data, session)
		return 'done'


@app.route('/static/<path:path>', methods=['GET'])
def file(filename):
	if os.path.isfile(fname):
		return app.send_static_file(filename)
	else:
		return abort(404)

@app.route('/', methods=['GET'])
def home():
	return app.send_static_file('index.html')


if __name__ == "__main__":
	app.run(debug=True)
