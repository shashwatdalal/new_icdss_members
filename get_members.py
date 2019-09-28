from datetime import datetime
import json
import os
import sys

import requests


def _get_s3_cids():
	# get list of Member's CID from s3
	
	with open('members.json') as f:
		s3_json = json.load(f)
	s3_cids = set()
	for period in s3_json['growth']:
		for cid in period['new_members']:
			s3_cids.add(cid)
	return s3_json, s3_cids

def _get_union_cids():
	# get list of Members's CID from Union API
	
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
	return union_cids

if __name__ == "__main__":
	# get previous member list
	s3_json, s3_cids = _get_s3_cids()
	# get updated member list
	union_cids = _get_union_cids()
	
	# calculate new sign-ups
	new_members = union_cids - s3_cids
	
	# update members json
	s3_json['growth'].append(
		{
			'timestamp': str(datetime.now()),
			'new_members': list(new_members), 
			'increase': len(new_members)
		}
	)
	with open('members.json', 'w') as f:
		json.dump(s3_json, f)
	

# # Get Slack URL
# slack_endpoint = sys.argv[2]

# # send update to slack channel
# message = {
# 	"blocks": [
# 		{
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": ":newspaper: *Number of signups*: {}".format(len(members))
# 			}
# 		}
# 	]
# }
# response = requests.post(slack_endpoint, json=message)
