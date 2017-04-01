import os, shutil, time
from user import User
from recieve import recieve

# Default values
send_to = 'http://0.0.0.0:8080/webhook'
page_id = 1

STOP_ON_FAIL = True
print 'STOP_ON_FAIL:', STOP_ON_FAIL
resultlist = []

# tools
def equals(got, expected):
	if expected == got:
		return [True, expected.replace('\n',' \ ')]
	else:
		return [False, expected, got]

def test(bol,win,fail):
	if bol:
		return [True,win]
	else:
		return [False,fail]

def clear_messages():
	if os.path.exists('messages'):
		shutil.rmtree('messages')

def addresult(res):
	resultlist.append(res)
	if res[0] is False and STOP_ON_FAIL:
		results()
		raise Exception('STOP ON FAIL')
	else:
		return res[0]

def results():
		print ''
		print 'RESULTS'
		print '-------'
		for res in resultlist:
			if res[0]:
				print 'PASSED:', res[1]
			else:
				if len(res) == 3:
					print 'FAILED: Expected', res[1], ' Got:', res[2]
				else:
					print res[1]

def timestamp():
	return int(time.time()*10**6)
