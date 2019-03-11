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

# [START gmail_quickstart]
"""
Shows basic usage of the Gmail API.

Lists the user's Gmail labels.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
# Setup the Gmail API
# SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'credentials.json'#'client_secrets.json'   # latest Google APIs renamed client_secrets.json file to credentials.json.
API_NAME = 'gmail'
def main(cred_file_dir, script_name):
    SCOPES = 'https://mail.google.com/'
    script_name = script_name.replace(' ','_').lower()
    # AUTH_FILE_NAME = 'credentials_gmail.json'       # this file name is normally client_credentails.json but name changed for multpile api support i.e gmail & drive
    # AUTH_FILE_NAME = script_name + '_credentials_' + API_NAME +'.json'
    AUTH_FILE_NAME = script_name + '_token_' + API_NAME +'.json'    # latest Google APIs renamed credentials.json file to token.json.
    store = file.Storage(os.path.join(cred_file_dir,AUTH_FILE_NAME))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(os.path.join(cred_file_dir,CLIENT_SECRET_FILE), SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    if not labels:
        print('No labels found.')
    else:
        pass
    return service
# [END gmail_quickstart]
