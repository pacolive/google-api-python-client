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
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Define Project Name 
    projectName = request.args.get('projectname')
    originFolder = request.args.get('originfolder')

    #destinationFolder = '1LN1_ZfANuOuEKjSIahjDBmwgx1V6-4qw'
    destinationFolder = '1elS4f5LqW0mvp0xTdTKbUYGOnGXMEuk5'

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

        # Get one of the templates
        page_token = None
        results = service.files().list(
        q=f"'{originFolder}' in parents",
        pageSize=10, fields="nextPageToken, files(id, name)",
        pageToken=page_token).execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        else:
            # Print the name of the file to move
            # print(u'{0} ({1})'.format(items[0]['name'], items[0]['id']))
            # Retrieve the existing parents to remove
            file = service.files().get(fileId=items[0]['id'], fields='parents').execute()
            previous_parents = ",".join(file.get('parents'))
            # Move the file to the new folder
            file = service.files().update(fileId=items[0]['id'], addParents=destinationFolder,
                                      removeParents=previous_parents,
                                      fields='id, parents').execute()
            # Rename the file
            body = {'name': projectName}
            service.files().update(fileId=items[0]['id'], body=body).execute()
            
            # Print amount of files in the folder
            print("Templates available: ",len(items) - 1)
            
            return
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

    return
# [END moveRenameFile]