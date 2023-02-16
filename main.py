from __future__ import print_function

import sys
import os.path
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import escape
import functions_framework


# [START moveRenameFile]
@functions_framework.http
def moveRenameFile(request):

    # Define credentials
    creds = None

    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']

    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = '1rQuZB_9PAjhD8YoueAXzfUoLLLg9CzAnX74TrWNfs6I'
    RANGE_NAME = 'URLWEBIA!A:B'

    success = "success"
    error = "error"

    # Define Template
    templateid = request.args.get('templateid')

    # Define Destination Folder
    destinationFolder = request.args.get('dest')

    # Define Project Name
    projectName = request.args.get('project')

    # Define Project Key
    projectKey = request.args.get('key')

    # Define File Name
    fileName = request.args.get('project') + str(projectKey)

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # call drive api client
        service = build('drive', 'v3', credentials=creds)

        # Clone the template
        newfile = {'name': fileName, 'parents' : [ { "id" : destinationFolder } ]}
        clone = service.files().copy(fileId=templateid, body=newfile).execute()

        # Retrieve the clone existing parents to remove
        file = service.files().get(fileId=clone.get('id'), fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))

        # Move the clone to the destination folder
        file = service.files().update(fileId=clone.get('id'), addParents=destinationFolder,
                                    removeParents=previous_parents,
                                    fields='id, parents').execute()
        
        # Apply general access permissions to file
        permission = {'type': 'anyone',
                'role': 'writer'}
        service.permissions().create(fileId=clone.get('id'),body=permission).execute()

        # Call sheets api client
        service = build('sheets', 'v4', credentials=creds)

        # Insert project data in spreadsheet
        rows = [projectName, "https://docs.google.com/spreadsheets/d/" + clone.get('id')],["", ""]
        resource = {
        "majorDimension": "ROWS",
        "values": rows
        }
        service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID,range=RANGE_NAME,body=resource,valueInputOption="USER_ENTERED").execute()
        
        return success

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')
    return success
# [END moveRenameFile]