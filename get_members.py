import codecs
import json
import os
import sys

import requests
import slack

# get api-keys 
token = sys.argv[1]
headers = {"X-API-Key": token}

# Imperial Union API end-point
END_POINT = 'https://eactivities.union.ic.ac.uk/API/CSP'

# get society code
response = requests.get(END_POINT, headers=headers)
society_code = json.loads(response.text)[0]['Code']

# get members 
year = '19-20'
members_url = os.path.join(END_POINT, society_code, 'reports', 'members?year={}'.format(year))
response = requests.get(members_url, headers=headers)
members = json.loads(response.text)

# Get Slack URL
slack_endpoint = sys.argv[2]
message = {
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "This is a plain text section block.",
				"emoji": True
			}
		}
	]
}
requests.post(slack_endpoint, message)
