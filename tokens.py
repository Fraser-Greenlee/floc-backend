import web
import os

TESTING = False

# database

def urltodb(url):
	url = url.replace('//','').replace('@',':').split(':')
	url[-1] = url[-1][url[-1].index('/')+1:]
	return web.database(dbn=url[0],db=url[4],user=url[1],pw=url[2],host=url[3])

LOCAL_TEST = False

# if remote test
DATABASE_URL = os.environ.get('HEROKU_POSTGRESQL_ROSE_URL')
# if live
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL is None:
	# if local
	LOCAL_TEST = True
	db = web.database(dbn='postgres',db='secret',user='postgres',pw='',host='localhost')
else:
	db = urltodb(DATABASE_URL)

## list of keys
webhook = 'kjhvvjhkvkgCGHgCJHjghcY6i7Cc7tt'
page = {
	'Test':'EAAFuDsxVFzwBAIm66ZClZAnt7tm58NwnK7z6wA4eZBMdPnb2bfxOX3i62cHrKa73TWnrYJ1aiWuZBYSJBTKtNR0zYTNdund8Y0tmDLwfg1YnZAlZCcBxKIvtIu29nagTICijZBbAC773eSx9rbk1r6m09iWCEcOcpcRX4bA6yM7UwZDZD',
	'Live':'EAAae68efi70BAPQUsusZCkfTm1KMRfETnLU3207hUMI5rywtFeKGe6plb7qpWybhKyVsu306fYC8ZA7fG9p7Mg4qi67KkP2XDqJ8ZAkUDg6ZCTYSDBiRQN8ZC48xcyV8voal8pXMyrg9VIfKtjiSEljYZC3QvsC11ZAwiJ7hXaKRQZDZD',
}

## keys in use

webhook_key = webhook
if LOCAL_TEST:
	print 'Local Testing'
	access_token = page['Test']
else:
	print 'Live'
	access_token = page['Live']
