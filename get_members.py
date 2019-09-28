import codecs
import json
import os
import sys

import requests

def _get_s3_cids(s3_json):
	old_cids = set()
	for period in s3_json['growth']:
		for cid in period['new_members']:
			old_cids.add(cid)
	return old_cids

# get api-keys 
token = sys.argv[1]
headers = {"X-API-Key": token}

# Imperial Union API end-point
END_POINT = 'https://eactivities.union.ic.ac.uk/API/CSP'

# get society code
response = requests.get(END_POINT, headers=headers)
society_code = json.loads(response.text)[0]['Code']

# get members from union api
year = '19-20'
members_url = os.path.join(END_POINT, society_code, 'reports', 'members?year={}'.format(year))
response = requests.get(members_url, headers=headers)
union_json = json.loads(response.text)
union_cids = set()
for member in union_json:
	union_cids.add(member['CID'])
print(union_cids)

# get previous members
with open('members.json') as f:
	s3_json = json.load(f)
old_cids = _get_s3_cids(s3_json)
print(old_cids)

# Get Slack URL
slack_endpoint = sys.argv[2]

# send update to slack channel
message = {
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":newspaper: *Number of signups*: {}".format(len(members))
			}
		}
	]
}
response = requests.post(slack_endpoint, json=message)
