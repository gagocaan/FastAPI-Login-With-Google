curl --request POST \
  'https://iap.googleapis.com/v1/projects/{project_number_id}/iap_web/appengine-{APP-ENGINE-ID}/services/{APP-ENGINE-ID}/versions/{APP-ENGINE-VERSION}:testIamPermissions' \
  --header 'Authorization: Bearer {ACCESS_TOKEN}' \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --data '{"permissions":["iap.webServiceVersions.accessViaIAP"]}' \
  --compressed