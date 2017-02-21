import web
import os

# database

def urltodb(url):#url = DATABASE_URL
	url = url.replace('//','').replace('@',':').split(':')
	url[-1] = url[-1][url[-1].index('/')+1:]
	return web.database(dbn=url[0],db=url[4],user=url[1],pw=url[2],host=url[3])

TEST = False
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL is None:
	# if not on heroku then testing
	TEST = True
	# goto local database
	db = web.database(dbn='postgres',db='secret',user='postgres',pw='',host='localhost')
else:
	print 'DATABASE_URL', DATABASE_URL
	db = urltodb(DATABASE_URL)

## list of keys
webhook = 'kjhvvjhkvkgCGHgCJHjghcY6i7Cc7tt'
page = {
	'SecretTestBot':'EAAFuDsxVFzwBANcbN1E5J4tgdwIYk2bDNYkQ5gSw11RtVNfFq5F5z5xCXG1OauqWnMrMHpi3EZCUDJenqoZBKs0VugcVwRCdeWiAws5WfedR2EfLUomSqfXeMfxQLrf2so0iGWkwlaU5XHEEITw8bdzayykNhuLSzRZC6933QZDZD',
	'SecretBotLiveTest':'EAAFuDsxVFzwBAF7y9LVZBwwKREkq4SxZCPXxCxFytB4KAZCDZCnvnpuYL4ne1aVjffyJjOaZB9yKwRgqrAqEDtZCq6D48E7pNffMNFNWzcW6Ih3i48bCrhCZCobvZCqjCnGZB6vNyYWZB2E0zaiKANcipYL4WwDCHvN8R818sSZCFZCTKAZDZD',
	'SecretBot':'EAAae68efi70BAPQUsusZCkfTm1KMRfETnLU3207hUMI5rywtFeKGe6plb7qpWybhKyVsu306fYC8ZA7fG9p7Mg4qi67KkP2XDqJ8ZAkUDg6ZCTYSDBiRQN8ZC48xcyV8voal8pXMyrg9VIfKtjiSEljYZC3QvsC11ZAwiJ7hXaKRQZDZD'
}

## keys in use

webhook_key = webhook
if TEST:
	access_token = page['SecretTestBot']
else:
	access_token = page['SecretBotLiveTest']
	#access_token = page['SecretBot']
