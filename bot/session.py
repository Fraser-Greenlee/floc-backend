
class Session(dict):
	def __init__(self, **cols):
		for key, value in cols.items():
			setattr(self, key, value)

	def set(self, **cols):# set values NOT updating database
		for name, value in cols.items():
			super(Session, self).__setattr__(name, value)

	def set_dict(self, cols):# set values NOT updating database
		for name, value in cols.items():
			super(Session, self).__setattr__(name, value)

	def update(self, **cols):# update values and database
		# update database values
		q = db.update('users', cols, where='id='+str(self.id))
		# update session values
		for name, value in cols.items():
			super(Session, self).__setattr__(name, value)
		# return query
		return q

	def update_dict(self, cols):# update values and database
		# update database values
		q = db.update('users', cols, where='id='+str(self.id))
		# update session values
		for name, value in cols.items():
			super(Session, self).__setattr__(name, value)
		# return query
		return q
