
from tokens import db

class Session(dict):
	def __init__(self, **cols):
		self.new_user = False
		self.status_bar = False
		for key, value in cols.items():
			setattr(self, key, value)

	@staticmethod
	def format_val(v):
		typ = type(v)
		if typ == str and v[0] == '$':
			v = v[1:]
			typ = 'raw'
		if typ == str:
			return "'"+v.replace("'","''")+"'"
		else:
			return str(v)

	def set(self, **cols):# set values NOT updating database
		for name, value in cols.items():
			super(Session, self).__setattr__(name, value)

	def set_dict(self, cols):# set values NOT updating database
		for name, value in cols.items():
			super(Session, self).__setattr__(name, value)

	def update(self, **cols):# update values and database
		return self.update_dict(cols)

	def update_dict(self, cols):# update values and database
		# update database values
		set_vals = ", ".join([col[0]+'='+self.format_val(col[1]) for col in cols.items()])
		q = db.query("UPDATE users SET "+set_vals+" WHERE id="+str(self.id))
		# update session values
		for name, value in cols.items():
			super(Session, self).__setattr__(name, value)
		# return query
		return q
#
