import codecs
import json
import os
import sys

import requests

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
slack_endpoint = "https://hooks.slack.com/services/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"
message = {
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":newspaper: New Sign-ups in the last *15 min*",
			}
		},
		{
			"type": "divider"
		}, 
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*{}*: {}".format(members[0]['CID'], members[0]['Login'])
			}
		}
	]
}
response = requests.post(slack_endpoint, json=message)
