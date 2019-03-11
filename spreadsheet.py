#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Client List Fetching from spreadsheet.

This Module fetch the data from the spreadsheets and accordingly stores it in list for further processing.

"""
from __future__ import print_function
import httplib2, os
from googleapiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'
API_NAME = 'spreadsheet'


def get_credentials(cred_file_dir, script_name):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    AUTH_FILE_NAME = script_name + '_credentials_' + API_NAME +'.json'
    credential_dir = cred_file_dir
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   AUTH_FILE_NAME)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(os.path.join(credential_dir,CLIENT_SECRET_FILE), SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main(cred_file_dir, script_name, spreadsheet_id, sheet_name = 'Sheet1'):
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    script_name = script_name.replace(' ','_').lower()
    credentials = get_credentials(cred_file_dir, script_name)
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = spreadsheet_id
    # rangeName = 'Sheet1!A2:Z200'    # source2:destination
    rangeName = '{}!A2:Z'.format(sheet_name)    # source2:destination
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        # print('CustomerId, Account Name')
        rows = []
        for row in values:
            rows.append(row)
        return rows

def get_accounts_data(cred_file_dir, script_name, spreadsheet_id,
                      sheet_name = 'Sheet1', required_customer_ids = [],
                      client_only = True):
    rows = main(cred_file_dir, script_name, spreadsheet_id, sheet_name)
    # print(rows[:5])
    account_managers = {}
    all_clients = {}
    for row in rows:
        if row!=[] and '-' in row[0]:
            if row[0]:#and row[3] == 'Yes':         # index 3 for WordOptimizer
                customer_id = row[0].replace('-','')
                # account_name = row[1]
                all_clients[customer_id] = dict({'spreadsheet_url':row[5]})
                # add whichever value needs to be added for e.g spreadsheet url
                if not client_only:
                    managers = row[8]
                    managers = managers.split(',')
                    for manager in managers:
                        if manager in account_managers:
                            account_managers[manager]['customers'].append(row[0].replace('-',''))
                        else:
                            account_managers[manager] = {'customers':[row[0].replace('-','')],
                                                         'message_text':'',
                                                         'color_no':0                              }

    # all_clients = {i[0].replace('-',''):i[1] for i in rows}
    if required_customer_ids != []:
        d = dict(all_clients)
        all_clients = {k:v for k,v in d.items() if k in required_customer_ids}
    if client_only:
        return all_clients
    return all_clients, account_managers


if __name__ == '__main__':
    main('CREDENTIALS/','1hoPoTuSvw_ZVpnA6RBxyYt3CSrdX1k0JU4sgYNvxWjE',
         'Sheet1!A2:Z200', sheet_name='Bid Optimizer Path-All Accounts [Master sheet]')