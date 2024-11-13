
---

# FCM Notification for Frappe using latest HTTP v1 API

This repository provides integration with Firebase Cloud Messaging (FCM) for sending push notifications from a Frappe/ERPNext instance. The app uses FCM's REST API to send notifications to client devices, leveraging Firebase service account credentials.

## Features

- **Push Notifications**: Send push notifications to Android and iOS devices using Firebase Cloud Messaging.
- **Access Token Management**: Automatically fetches and caches access tokens to reduce API calls.
- **Customizable Notification Settings**: Configurable FCM Notification Settings for managing Firebase service account credentials.

---

## Important Note
For testing purposes, the code is currently configured to send notifications via FCM topics instead of device tokens. The device token-based notification payload is commented out in the send_fcm_notification function to allow easier testing with a topic-based approach. If you wish to switch back to device-specific notifications, uncomment the device_token code block and adjust the payload accordingly.

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
1. Link your device id to each user using the User Device DocType.
2. Create a notification in Frappe/ERPNext (https://docs.erpnext.com/docs/user/manual/en/notifications)
3. Run an event that triggers any notification. The notifcation will be send the respetive user via FCM if they have subscribed to it.
4. Optionally you can use whitelisted method `api/method/frappe_fcm_notification.fcm_notification.notification_queue` to test in postman.


### Logging and Error Handling

- Errors are logged in **Error Logs** in Frappe, allowing you to view and debug any issues that occur during notification sending.
- You can limit the length of logged access tokens to prevent security issues (e.g., only logging the first 50 characters).


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
