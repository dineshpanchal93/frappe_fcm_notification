# Copyright (c) 2024, Upscape Technologies and contributors
# For license information, please see license.txt

import frappe
import requests
import json
from frappe.model.document import Document
from frappe_fcm_notification.fcm_notification import get_cached_access_token


class UserDevice(Document):
	
	def after_insert(self):

		if self.device_type == "ios":
			self.device_token = get_ios_device_token(self.device_token)
			frappe.log_error(f"Device Token: {self.device_token}","Device Token")
			self.save()

@frappe.whitelist(allow_guest=True)
def get_ios_device_token(device_token):
	print("inside get_ios_device_token")
	print(device_token)
	access_token = get_cached_access_token()
	
	# frappe.log_error(f"access_token: {access_token}","Access")

	url = "https://iid.googleapis.com/iid/v1:batchImport"

	payload = json.dumps({
		"application": "com.upscape.crm",
		"sandbox":False,
		"apns_tokens":[device_token]
	})

	headers = {
		'access_token_auth': 'true',
		'Content-Type': 'application/json',
		'Authorization': f'Bearer {access_token["access_token"]}'
	}

	response = requests.post(url, headers=headers, data=payload)
	frappe.log_error(f"Response: {response.text}","Response")
	frappe.log_error(f"Response2: {response}","Response")

	

	if response.status_code == 200:
		return response.text


