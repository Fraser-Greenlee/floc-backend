import web
import os

# database

def urltodb(url):
	url = url.replace('//','').replace('@',':').split(':')
	url[-1] = url[-1][url[-1].index('/')+1:]
	return web.database(dbn=url[0],db=url[4],user=url[1],pw=url[2],host=url[3])

LOCAL_TEST = False

# if remote test
DATABASE_URL = os.environ.get('HEROKU_POSTGRESQL_ROSE_URL')
REMOTE_TEST = DATABASE_URL is not None
if REMOTE_TEST is False:
	# if live
	DATABASE_URL = os.environ.get('DATABASE_URL')
	if DATABASE_URL is None:
		# if local
		LOCAL_TEST = True
		db = web.database(dbn='postgres',db='secret',user='postgres',pw='',host='localhost')
	else:
		db = urltodb(DATABASE_URL)
else:
	db = urltodb(DATABASE_URL)

## list of keys
webhook = 'kjhvvjhkvkgCGHgCJHjghcY6i7Cc7tt'
page = {
	'Test':'EAAFuDsxVFzwBACGpc5UdzgIZB6CNlGuW1FbuCqYRN7OnXUwRq6KvGyHmP8mGbnqTL2cMHnFkVKj4uFCW6spSGWWFx9IgwenwsXE3iCpqwXbyW3HPewsgVX0sN4AHG5noOTbed4bqHHVgrZAwZCu3kSbd5RolfuWYHrFcdgwJAZDZD',
	'RemoteTest':'EAAU5ILKtVX8BAEQNJu3s8QcbE5bmw79PVzZAY4yKPkwSZBzihaJLUUe2FmuDPGspBNNBxNJ2auZB9O1IPweSQ4L8ZCiHC8w72ZA6yUdey4LHjSuqglEisgzFFr8sXbaremC9qXn5RRQiAhogJCaFT8YZBOL2gLFWvMLk5ck37m2AZDZD',
	'Live':'EAAae68efi70BAPQUsusZCkfTm1KMRfETnLU3207hUMI5rywtFeKGe6plb7qpWybhKyVsu306fYC8ZA7fG9p7Mg4qi67KkP2XDqJ8ZAkUDg6ZCTYSDBiRQN8ZC48xcyV8voal8pXMyrg9VIfKtjiSEljYZC3QvsC11ZAwiJ7hXaKRQZDZD'
}

## keys in use

webhook_key = webhook
if LOCAL_TEST:
	print 'Local Testing'
	access_token = page['Test']
elif REMOTE_TEST:
	print 'Remote Testing'
	access_token = page['RemoteTest']
else:
	print 'Live'
	access_token = page['Live']
