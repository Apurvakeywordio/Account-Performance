# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START drive_quickstart]
"""
Shows basic usage of the Drive v3 API.

Creates a Drive v3 API service and prints the names and ids of the last 10 files
the user has access to.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os


CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'drive'

def main(cred_file_dir, script_name):
    # Setup the Drive v3 API
    SCOPES = 'https://www.googleapis.com/auth/drive'
    # api_access_file_name = 'credentials_drive.json'     # this file name is normally client_credentails.json but name changed for multpile api support i.e gmail & drive
    AUTH_FILE_NAME = script_name + '_credentials_' + API_NAME +'.json'
    store = file.Storage(os.path.join(cred_file_dir,AUTH_FILE_NAME))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(os.path.join(cred_file_dir,CLIENT_SECRET_FILE), SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        pass
#         print('Files:')
#         for item in items:
#             print('{0} ({1})'.format(item['name'], item['id']))
    # [END drive_quickstart]
    return service
