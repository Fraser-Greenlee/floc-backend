import bot
from flask import Flask, request, abort, send_from_directory
import os.path

app = Flask(__name__)


@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
	if request.method == 'GET':
		return bot.verify(request)
	elif request.method == 'POST':
		session = bot.Session(id=None, current_msg='Start', location=0, lat=0, long=0, open_group=0, recieve_messages=True, temp_group_id=0, group_name='', last_sent=0, last_time=0, identity=0, quick_replies='')
		bot.recieve(request.data, session)
		return 'done'


@app.route('/static/<path:path>', methods=['GET'])
def file(filename):
	print 'file'
	if os.path.isfile(fname):
		return app.send_static_file(filename)
	else:
		return abort(404)

@app.route('/', methods=['GET'])
def home():
	print 'home'
	return app.send_static_file('index.html')


if __name__ == "__main__":
	app.run(debug=True)
