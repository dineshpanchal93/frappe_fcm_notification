
---

# FCM Notification for Frappe

This repository provides integration with Firebase Cloud Messaging (FCM) for sending push notifications from a Frappe/ERPNext instance. The app uses FCM's REST API to send notifications to client devices, leveraging Firebase service account credentials.

## Features

- **Push Notifications**: Send push notifications to Android and iOS devices using Firebase Cloud Messaging.
- **Access Token Management**: Automatically fetches and caches access tokens to reduce API calls.
- **Customizable Notification Settings**: Configurable FCM Notification Settings for managing Firebase service account credentials.

---

## Installation

### Prerequisites

- Ensure your Frappe/ERPNext environment is running.

### Step 1: Clone the Repository

```bash
cd /path/to/frappe-bench/apps
git clone https://github.com/fadilsiddique/frappe_fcm_notification.git
```

### Step 2: Install the App in Your Site

```bash
cd /path/to/frappe-bench
bench install-app frappe_fcm_notification
```

### Step 3: Apply Changes

```bash
bench migrate
bench restart
```

---

## Configuration

### Step 1: Obtain Service Account Credentials

1. In your [Firebase Console](https://console.firebase.google.com/), go to **Project Settings > Service accounts**.
2. Click **Generate new private key**. This downloads a JSON file containing your service account credentials and firebase admin-sdk credentials.

### Step 2: Set Up FCM Notification Settings

#### Add Values from `project-name-firebase-adminsdk-8uf66-eagb4660e2.json`

The app expects FCM Notification Settings values to be filled in with data from admin-sdk json file, the file name should look like `project-name-firebase-adminsdk-8uf66-eagb4660e2.json`. 
Follow these steps to configure FCM Notification Settings in your Frappe/ERPNext instance:

1. Go to **Frappe > Settings > FCM Notification Settings** in your Frappe instance.
2. Populate the following fields using the values from your `service_token.json` file:

   - `Project ID`: `"project_id"` from JSON
   - `Private Key ID`: `"private_key_id"` from JSON
   - `Private Key`: `"private_key"` from JSON (replace `\\n` with actual newline characters)
   - `Client Email`: `"client_email"` from JSON
   - `Client ID`: `"client_id"` from JSON
   - `Auth URI`: `"auth_uri"` from JSON
   - `Token URI`: `"token_uri"` from JSON
   - `Auth Provider X509 Cert URL`: `"auth_provider_x509_cert_url"` from JSON
   - `Client X509 Cert URL`: `"client_x509_cert_url"` from JSON

3. Save the settings.

---

## Usage

### Sending a Notification

Once the settings are configured, you can send notifications through the following API endpoints:



1. **Send FCM Notification**

   Endpoint: `/api/method/frappe_fcm_notification.fcm_notification.notification_queue`

   **Parameters**:
   - `device_token`: The device token of the recipient.
   - `title`: The title of the notification.
   - `body`: The body text of the notification.

   **Example**:

   ```json
   {
       "device_token": "device_token_value",
       "title": "Hello",
       "body": "This is a test notification."
   }
   ```

   **Response**:

   ```json
   {
       "status": "success",
       "response": {
           "name": "projects/your-project-id/messages/message-id"
       }
   }
   ```

### Logging and Error Handling

- Errors are logged in **Error Logs** in Frappe, allowing you to view and debug any issues that occur during notification sending.
- You can limit the length of logged access tokens to prevent security issues (e.g., only logging the first 50 characters).

### Example Code Snippets

#### Fetching FCM Credentials

```python
@frappe.whitelist()
def get_fcm_credentials():
    credentials_doc = frappe.get_single("FCM Notification Settings")
    return {
        "type": "service_account",
        "project_id": credentials_doc.get("project_id"),
        "private_key_id": credentials_doc.get("private_key_id"),
        "private_key": credentials_doc.get_password("private_key").replace("\\n", "\n"),
        "client_email": credentials_doc.get("client_email"),
        "client_id": credentials_doc.get("client_id"),
        "auth_uri": credentials_doc.get("auth_uri"),
        "token_uri": credentials_doc.get("token_uri"),
        "auth_provider_x509_cert_url": credentials_doc.get("auth_provider_x509_cert_url"),
        "client_x509_cert_url": credentials_doc.get("client_x509_cert_url")
    }
```

#### Sending a Notification

```python
@frappe.whitelist()
def send_fcm_notification(device_token, title, body):
    access_token = get_cached_access_token()["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; UTF-8",
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
    fcm_endpoint = f'https://fcm.googleapis.com/v1/projects/{get_fcm_credentials()["project_id"]}/messages:send'
    response = requests.post(fcm_endpoint, headers=headers, json=payload)
    if response.status_code == 200:
        return {"status": "success", "response": response.json()}
    else:
        frappe.log_error(response.text, "FCM Notification Error")
        return {"status": "failed", "error": response.text}
```

---

## Troubleshooting

1. **Invalid Device Token**: Ensure that the device token provided is valid and registered with FCM.
2. **Authentication Issues**: Verify the `service_token.json` credentials and check that the token URI and other settings in **FCM Notification Settings** match.
3. **Access Token Expiration**: Access tokens are cached for 55 minutes; however, if tokens expire sooner, revalidate the token cache logic.

---

## License

This project is licensed under the MIT License.

--- 

## Contributing

Feel free to submit pull requests and issues. Contributions are welcome!

---
