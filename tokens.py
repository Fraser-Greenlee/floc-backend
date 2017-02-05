import web
import os

# database

def urltodb(url):
	url = url.replace('//','').replace('@',':').split(':')
	url[-1] = url[-1][url[-1].index('/')+1:]
	return web.database(dbn=url[0],db=url[4],user=url[1],pw=url[2],host=url[3])


DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL is None:
	# if not on heroku then testing
	TEST = True
	DATABASE_URL = 'postgres://tatvwdylfhnthu:9aa3223d040c65ef06e9362022004fe9bb5b3e3f44b67ad4101f549fddaa8177@ec2-54-204-1-40.compute-1.amazonaws.com:5432/d8bqtbsqkdmogn'

db = urltodb(DATABASE_URL)


## list of keys
webhook = 'kjhvvjhkvkgCGHgCJHjghcY6i7Cc7tt'
page = {
	'SecretTestBot':'EAAFuDsxVFzwBAKtf0h72iT1iP5yMC2AZByuwBprcTZAXGwdAn0PNiFMwncu9HZBZBuSflpAfx5ANAYkOL0FS8sdc0YJJRtlWyV7YvZB0CotrqyVDtsYyaz3SOZB024lUsqCWXHxf416CDdZBO4tU7GkuO5dS65BFaGJGbt0BYqJpgZDZD',
	'SecretBot':'EAAae68efi70BAFfaPF9zCQCS0RquK21hQRQWInZBja2WbEPhUVCiBvg3n9AHZAphCZBkvVIBYOj7uDNDAUAM19GtZBZC0bNZBJZBse9nqYn0PzdlZBXCzuhV4NKhfA8RFuJyf9VSGcWeLZCrUma4AheUzXvSifVMEIq4rq7kj1cbVDQZDZD'
}

## keys in use

webhook_key = webhook
if TEST:
	access_token = page['SecretTestBot']
else:
	access_token = page['SecretBot']
