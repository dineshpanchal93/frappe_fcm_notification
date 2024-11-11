import json
import requests
import frappe
from google.oauth2 import service_account
from frappe.utils import now, add_to_date

@frappe.whitelist()
def get_fcm_credentials():
    """
    Retrieves FCM credentials from FCM Notification Settings DocType.
    """
    credentials_doc = frappe.get_single("FCM Notification Settings")
    service_account_info = {
        "type": "service_account",
        "project_id": credentials_doc.get("project_id"),
        "private_key_id": credentials_doc.get("private_key_id"),
        "private_key": credentials_doc.get_password("private_key").replace("\\n", "\n").strip(),
        "client_email": credentials_doc.get("client_email"),
        "client_id": credentials_doc.get("client_id"),
        "auth_uri": credentials_doc.get("auth_uri"),
        "token_uri": credentials_doc.get("token_uri"),
        "auth_provider_x509_cert_url": credentials_doc.get("auth_provider_x509_cert_url"),
        "client_x509_cert_url": credentials_doc.get("client_x509_cert_url")
    }
    return service_account_info

@frappe.whitelist()
def get_cached_access_token():
    """
    Retrieves the cached access token if valid, otherwise generates a new one.
    """
    # Fetch the FCM Notification Settings DocType
    credentials_doc = frappe.get_single("FCM Notification Settings")
    
    # Check if there is a valid access token
    if credentials_doc.access_token and credentials_doc.expiration_time > now():
        return credentials_doc.access_token

    # Generate a new access token if expired or missing
    service_account_info = get_fcm_credentials()
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=["https://www.googleapis.com/auth/firebase.messaging"]
    )

    frappe.log_error(frappe.get_traceback(), f"007 {credentials}")
    frappe.log_error( f"008 {credentials.token}","FCM Token")
    access_token = credentials.token
    expiration_time = add_to_date(now(), minutes=55)  # Set expiration about an hour from now

    # Update the FCM Notification Settings DocType with new token and expiration time
    credentials_doc.access_token = access_token
    credentials_doc.expiration_time = expiration_time
    credentials_doc.save()
    frappe.db.commit()

    return {"access_token": access_token}

@frappe.whitelist()
def send_fcm_notification(device_token, title, body):
    """
    Sends a push notification using the cached access token.
    """
    access_token = get_cached_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; UTF-8',
    }
    payload = {
        "message": {
            "token": device_token,
            "notification": {
                "title": title,
                "body": body
            },
            "data": {
                "click_action": "FLUTTER_NOTIFICATION_CLICK",
                "title": title,
                "body": body
            }
        }
    }

    # Send notification via Firebase Cloud Messaging
    fcm_endpoint = f'https://fcm.googleapis.com/v1/projects/{get_fcm_credentials()["project_id"]}/messages:send'
    response = requests.post(fcm_endpoint, headers=headers, json=payload)
    
    # Check response status
    if response.status_code == 200:
        frappe.log("Notification sent successfully:", response.json())
        return {"status": "success", "response": response.json()}
    else:
        error_message = f"Failed to send notification: {response.text}"
        frappe.log_error(error_message, "FCM Notification Error")
        return {"status": "failed", "error": error_message}
