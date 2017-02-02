
import bot

class Start:
	@staticmethod
	def start(id):
		return False

	@staticmethod
	def recieve(db,id,msg):
		bot.send(
			id,
			"""Welcome to Secret.\nA place for ananymous group chats on Messenger."""
		)
		bot.setmessage(db,id,'chat')


class Chat:
	@staticmethod
	def start(id):
		return False

	@staticmethod
	def recieve(db,id,msg):
		# send message to all other users
		q = db.query("SELECT id FROM users WHERE id<>"+str(id))
		idlist = []
		for r in q:
			idlist.append(r['id'])
		# send to all ids in list
		bot.send(
			idlist,
			msg
		)
