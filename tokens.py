import web
import os

# database

def urltodb(url):
	url = url.replace('//','').replace('@',':').split(':')
	url[-1] = url[-1][url[-1].index('/')+1:]
	return web.database(dbn=url[0],db=url[4],user=url[1],pw=url[2],host=url[3])


DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL is None:
	DATABASE_URL = 'postgres://tatvwdylfhnthu:9aa3223d040c65ef06e9362022004fe9bb5b3e3f44b67ad4101f549fddaa8177@ec2-54-204-1-40.compute-1.amazonaws.com:5432/d8bqtbsqkdmogn'

db = urltodb(DATABASE_URL)


## list of keys

test = 'kjhvvjhkvkgCGHgCJHjghcY6i7Cc7tt'
page = {
	'SecretTestBot':'EAAFuDsxVFzwBAKtf0h72iT1iP5yMC2AZByuwBprcTZAXGwdAn0PNiFMwncu9HZBZBuSflpAfx5ANAYkOL0FS8sdc0YJJRtlWyV7YvZB0CotrqyVDtsYyaz3SOZB024lUsqCWXHxf416CDdZBO4tU7GkuO5dS65BFaGJGbt0BYqJpgZDZD'
}

## keys in use

# for testing
webhook_key = test
access_token = page['SecretTestBot']
