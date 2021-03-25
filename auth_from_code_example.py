import json
import requests
from google_auth_oauthlib import flow

launch_browser = True

appflow = flow.InstalledAppFlow.from_client_secrets_file(
    "path/to/secret_file.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

if launch_browser:
    appflow.run_local_server(host="127.0.0.1")
else:
    appflow.run_console()

credentials = appflow.credentials

headers = {
    "Authorization": f"Bearer {credentials.token}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}
print(headers)
payload = json.dumps({"permissions": ["iap.webServiceVersions.accessViaIAP"]})
response = requests.post(
    "https://iap.googleapis.com/v1/projects/{project_number_id}/iap_web/appengine-{APP-ENGINE-ID}/services/{APP-ENGINE-ID}/versions/{APP-ENGINE-VERSION}:testIamPermissions",
    headers=headers,
    data=payload,
)
print(response.text)
