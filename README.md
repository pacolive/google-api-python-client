# google-api-python-client
Uses the Google Drive API to rename files and move them to a different folder

Deploy app locally
functions-framework --target=moveRenameFile --signature-type=event --debug --port=80

Test app locally
http://127.0.0.1/?projectname=https://script.google.com/-FODAWEBIA&originfolder=1LN1_ZfANuOuEKjSIahjDBmwgx1V6-4qw

Deploy app to GCP
gcloud functions deploy webia --gen2 --runtime=python310 --region=us-central1 --source=. --entry-point=moveRenameFile --trigger-http --allow-unauthenticated

Test app online
https://app/?projectname=https://script.google.com/-CANVASWEBIA&originfolder=1LN1_ZfANuOuEKjSIahjDBmwgx1V6-4qw