import web
import os

REMOTE_TEST_DB_URL = 'postgres://tatvwdylfhnthu:9aa3223d040c65ef06e9362022004fe9bb5b3e3f44b67ad4101f549fddaa8177@ec2-54-204-1-40.compute-1.amazonaws.com:5432/d8bqtbsqkdmogn'

# database

def urltodb(url):#url = DATABASE_URL
	url = url.replace('//','').replace('@',':').split(':')
	url[-1] = url[-1][url[-1].index('/')+1:]
	return web.database(dbn=url[0],db=url[4],user=url[1],pw=url[2],host=url[3])

LOCAL_TEST = False
DATABASE_URL = os.environ.get('DATABASE_URL')
REMOTE_TEST = DATABASE_URL == REMOTE_TEST_DB_URL
if DATABASE_URL is None:
	# if not on heroku then testing
	LOCAL_TEST = True
	# goto local database
	db = web.database(dbn='postgres',db='secret',user='postgres',pw='',host='localhost')
else:
	print 'DATABASE_URL', DATABASE_URL
	db = urltodb(DATABASE_URL)

## list of keys
webhook = 'kjhvvjhkvkgCGHgCJHjghcY6i7Cc7tt'
page = {
	'SecretTestBot':'EAAFuDsxVFzwBACGpc5UdzgIZB6CNlGuW1FbuCqYRN7OnXUwRq6KvGyHmP8mGbnqTL2cMHnFkVKj4uFCW6spSGWWFx9IgwenwsXE3iCpqwXbyW3HPewsgVX0sN4AHG5noOTbed4bqHHVgrZAwZCu3kSbd5RolfuWYHrFcdgwJAZDZD',
	'SecretBotLiveTest':'EAAFuDsxVFzwBAF7y9LVZBwwKREkq4SxZCPXxCxFytB4KAZCDZCnvnpuYL4ne1aVjffyJjOaZB9yKwRgqrAqEDtZCq6D48E7pNffMNFNWzcW6Ih3i48bCrhCZCobvZCqjCnGZB6vNyYWZB2E0zaiKANcipYL4WwDCHvN8R818sSZCFZCTKAZDZD',
	'SecretBot':'EAAae68efi70BAPQUsusZCkfTm1KMRfETnLU3207hUMI5rywtFeKGe6plb7qpWybhKyVsu306fYC8ZA7fG9p7Mg4qi67KkP2XDqJ8ZAkUDg6ZCTYSDBiRQN8ZC48xcyV8voal8pXMyrg9VIfKtjiSEljYZC3QvsC11ZAwiJ7hXaKRQZDZD'
}

## keys in use

webhook_key = webhook
if LOCAL_TEST:
	access_token = page['SecretTestBot']
elif REMOTE_TEST:
	access_token = page['SecretBotLiveTest']
else:
	access_token = page['SecretBot']
