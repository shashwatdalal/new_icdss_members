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

def _get_union_data():
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
	union_cids = []
	union_emails = []
	for member in union_json:
		union_cids.append(member['CID'])
		union_emails.append(member['Email'])
	return union_cids, union_emails

def _update_s3(new_members, s3_json):
	# update members json
	s3_json['growth'].append(
		{
			'timestamp': str(datetime.now()),
			'new_members': new_members, 
			'increase': len(new_members)
		}
	)
	with open('members.json', 'w') as f:
		json.dump(s3_json, f)

def _send_slack_message(new_members):
	# Get Slack URL
	slack_endpoint = sys.argv[2]

	# send update to slack channel
	message = {
		"blocks": [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": ":newspaper: *Number of New Signups*: {}".format(len(new_members))
				}
			}
		]
	}
	response = requests.post(slack_endpoint, json=message)
	
def _update_mailchimp(new_emails):
	ICDSS_19_20_ID = '08aad186c9'
	API_KEY = sys.argv[3]
	URL = 'https://us18.api.mailchimp.com/3.0/lists/{}/members'.format(ICDSS_19_20_ID)
	auth = ('my_username', API_KEY)
	for email in new_emails:
		response = requests.post(URL, auth=auth, json={
			'email_address': email, 
			'status': 'subscribed'
		})
		if response.status_code != 200:
			print('Failed to add ', email)

if __name__ == "__main__":
	# get data from two sources
	s3_json, s3_cids = _get_s3_cids()
	union_cids, union_emails = _get_union_data()
	
	# calculate new sign-ups
	new_member_idx = []
	for i, union_cid in enumerate(union_cids):
		if union_cid not in s3_cids:
			new_member_idx.append(i)
	new_members_cid = [union_cids[i] for i in new_member_idx]
	new_members_email = [union_emails[i] for i in new_member_idx]
	
	_update_s3(new_members_cid, s3_json)
	_send_slack_message(new_members)
	_update_mailchimp(new_members_email)
