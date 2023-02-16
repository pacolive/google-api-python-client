# google-api-python-client
Uses the Google Drive API to rename files and move them to a different folder

Deploy app locally
functions-framework --target=moveRenameFile --signature-type=event --debug --port=80

Test app locally
http://127.0.0.1/?project=https://script.google.com/&key=-FODAWEBIA&templateid=13RcZSTwQnTJc2gIsFi6zvBWsBQvMf5H1mOi7en4mz-E&dest=1elS4f5LqW0mvp0xTdTKbUYGOnGXMEuk5

Deploy app to GCP
gcloud functions deploy webia --gen2 --runtime=python310 --region=us-central1 --source=. --entry-point=moveRenameFile --trigger-http --allow-unauthenticated

Test app online
https://app/?project=https://script.google.com/&key=-FODAWEBIA&templateid=13RcZSTwQnTJc2gIsFi6zvBWsBQvMf5H1mOi7en4mz-E&dest=1elS4f5LqW0mvp0xTdTKbUYGOnGXMEuk5