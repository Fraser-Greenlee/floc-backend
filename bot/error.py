class SendError:
	def __init__(self,jsn):
		self.message = jsn['message']
		self.code = jsn['code']
		self.type = jsn['type']
		self.fbtrace_id = jsn['fbtrace_id']
		self.error_subcode = jsn['error_subcode']
		self.jsn = jsn
	def __str__(self):
		return str(self.jsn)
#
