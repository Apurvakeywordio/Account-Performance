#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Business Logic module.

This modules deals with the logic which script is executing to serve the required purpose.

Todo:
    * For Performing the manipulations on the data.
    * To calculate and decide the values to set in live to an account.
"""
from . import  auth_flow
import os
from apiclient.http import MediaFileUpload
import datetime as dt


def get_email_credentials_from_file(filename):
    email_data = {}
    s = ""
    with open(filename,'r') as f:
        lines = f.readlines()
        for i,line in enumerate(lines):
            if 'email_body' in line:
                for j in lines[i+1:]:
                    s = s +j
                email_data['email_body'] = s
            elif ":" in line:
                l = line[:-1].split(':')
                email_data[l[0]] = l[1]
    return email_data

def create_folder(drive_service, folder_name, parent_id):
    folder_id = check_folder_exists(drive_service, folder_name, parent_id)
    if folder_id:           # Folder exists
        print(folder_name,'folder already exists')
        folder = drive_service.files().get(fileId = folder_id).execute()
        print(folder)
        return folder['id']
    else:                   # Folder does not exists then create new
        file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id != None:           # if parent_id is None then folder is created at root directory of drive
            file_metadata['parents'] = [parent_id]
            print(file_metadata)
        file = drive_service.files().create(body=file_metadata,
                                            fields='id').execute()
        print(file)
        return file.get('id')

def check_folder_exists(drive_service, folder_name, parent_id):
    query =""" name='{}' """.format(folder_name)
    if parent_id != None:
        print('PARENT = ',parent_id)
        query =""" name='{}' and '{}' in parents """.format(folder_name, parent_id)
    print('QUERY = ',query)
    response = drive_service.files().list(q = query).execute()
    if response['files']==[]:
        print('  {} not found \nit will be created'.format(folder_name))
        return False        # Folder does not exist so return False
    for file in response.get('files', []):
        print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
        folder_id = file.get('id')
    return folder_id        # Folder exists so return FolderId

def inserting_a_file(drive_service, folder_id, filename, file_path):
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    path = os.path.join(file_path, filename)
    file_extension = filename.split('.')[-1]
    if file_extension=='csv':
        mimetype = 'text/csv'
    elif file_extension=='sql':
        mimetype = 'text/sql'
    print(filename,mimetype)
    media = MediaFileUpload(path,
                            mimetype=mimetype,
                            resumable=True)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))
    return file.get('id')

def get_email_credentials_from_file(filename):
    email_data = {}
    s = ""
#     print(filename)
    with open(filename,'r') as f:
        lines = f.readlines()
        for i,line in enumerate(lines):
            if 'email_body' in line:
                for j in lines[i+1:]:
#                     print(j)
                    s = s +j
                email_data['email_body'] = s
            elif ":" in line:
                l = line[:-1].split(':')
                email_data[l[0]] = l[1]
#                 print(line[:-1].split(':'))
    return email_data


def callback(request_id, response, exception):
    if exception:
        # Handle error
        print(exception)
    else:
        print("Permission Id: %s" % response.get('id'))

def set_folder_permission(drive_service, folder_id, email_ids):
    batch = drive_service.new_batch_http_request(callback=callback)
    role = "reader"        # type of permission for shared file
    for email_id in email_ids:
        print(email_id,'-->','readers')
        user_permission = {
        'type': 'user',
        'role': role,
        'emailAddress': email_id
        }
        batch.add(drive_service.permissions().create(
                fileId=folder_id,
                body=user_permission,
                fields='id'))
        batch.execute()


def main(cred_file_dir,filepath,filenames, script_name):
    # path = os.path.abspath(__file__)
    # path = os.path.dirname(path)   # path points to 'drive_module' folder
    # path = os.path.dirname(path)   # path points to  parent folder 'drive_module' folder which contains 'CREDENTIALS' folder and main module which calls the email module
    # print('PATH = ',path)
    # credentials_folder_name = "CREDENTIALS"     # name of folder which contains credentials files
    # cred_file_dir = os.path.join(path,credentials_folder_name)
    print('credentials path = ',cred_file_dir)
    email_data_filename = 'email_data.txt'          # name of file which contains details of email to be sent eg: sender, receiver, email subject
    email_data = get_email_credentials_from_file(os.path.join(cred_file_dir,email_data_filename))
    print('email data--->\n',email_data)
    drive_service = auth_flow.main(cred_file_dir, script_name)
    print('Drive Service = ',drive_service)
    drive_backup_folder_name = 'backups'
    root_folder_id = create_folder(drive_service, drive_backup_folder_name, None)     #'None' is passed for 'parent_id' as backup folder should be at root level of drive
    # create a folder for today's date
    d = dt.datetime.now()
    todays_date_folder_name = d.strftime('%d-%b-%y')
    folder_id = create_folder(drive_service, todays_date_folder_name, root_folder_id)   # Backup folder id(root_folder_id) is passed as parent_id
    for filename in filenames:
        file_id = inserting_a_file(drive_service, folder_id, filename, filepath)
    to = email_data['receiver_email_address']                                # Email address of the receivers.
    email_ids = to.split(',')
    set_folder_permission(drive_service, folder_id, email_ids)
    shareable_link = 'https://drive.google.com/open?id='
    return [shareable_link+folder_id, todays_date_folder_name]


if __name__=='__main__':
    filenames = ['Account_analysis_brand_campaign_data.xlsx']#, 'Account_analysis_all_campaign_data.xlsx', 'Account_analysis_shopping_campaign_data.xlsx']
    # The name of the file/files to be attached.
    file_dir = ''                   # The directory containing the file to be attached.
    main(filepath,filenames)

## How to use this API module
# first import  this module in your main script as follows
# from APIModules.drive_module import main as upd
# Call this module's main function as follows
# upd.main(cred_file_dir, filepath, filenames, SCRIPT_NAME)
# cred_file_dir is folder path of CREDENTIALS folder
