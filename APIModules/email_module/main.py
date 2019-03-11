import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import mimetypes
import os
from . import  auth_flow

from apiclient import errors


def SendMessage(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)



def CreateMessageWithAttachments(sender, to, cc, subject, message_text, filepath,
                                filenames, html):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    if cc:
        message['cc'] = cc

    if html:
        msg = MIMEText(message_text,'html')
    else:
        msg = MIMEText(message_text)

    message.attach(msg)

    for filename in filenames:      # attaching files to message
        file_path = os.path.join(filepath, filename)
        attachment = MIMEApplication(open(file_path,'rb').read(), _subtype = 'txt')
        attachment.add_header('Content-Disposition', 'attachment', filename = filename)
        message.attach(attachment)


    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def get_email_credentials_from_file(filename):
    email_data = {}
    s = ""
#     print(filename)
    with open(filename,'r') as f:
        lines = f.readlines()
        for i,line in enumerate(lines):
            if 'email_body' in line:
                for j in lines[i+1:-1]:
#                     print(j)
                    s = s +j
                email_data['email_body'] = s
            elif ":" in line:
                l = line[:-1].split(':')
                email_data[l[0]] = l[1]
#                 print(line[:-1].split(':'))
    return email_data


def main(cred_file_dir,filepath,filenames, script_name, to = None, subject = None, message_text = None, html =True, cc = None):
    """Send email after creating attachments to respective receiver.

    Args:
        filepath: path of folder which contains files to be attached in email

        filenames: name of files to be attached

        to = string of comma separated one or more emailids of receiver (optional)

        cc = emailid of cc (optional)

        subject = subject of email (optional)

        message_text = message body of email (optional)

        html = boolean value denoting type of email should html or not. default is False.(optional)

    Returns:
      A message object of mail sent.

    optional parameters like to, subject, message_text are taken from file named 'email_data.txt' which must be stored in 'CREDENTIALS' folder.
    whereas html parameter is optional but must be set to True if required type of email is HTML.
    """


    print('credentials path = ',cred_file_dir)
    email_data_filename = 'email_data.txt'          # name of file which contains details of email to be sent eg: sender, receiver, email subject
    f = open(os.path.join(cred_file_dir,email_data_filename),'r').read()


    email_data = get_email_credentials_from_file(os.path.join(cred_file_dir,email_data_filename))
    # print('email data--->\n',email_data)
    files = os.listdir(cred_file_dir)

    sender = email_data['sender_email_address']                             # Email address of the sender.
    if to==None:
        to = email_data['receiver_email_address']
    if cc==None:
        cc = email_data['cc_email_address']                                # Email address of the receiver.
        if cc==None or cc=='':
            print('cc = ',cc)
            cc = None
    if subject == None:
        subject = email_data['email_subject']                      # The subject of the email message.
    if message_text == None:
        message_text = email_data['email_body']
    if '"'==message_text[-1]:
        message_text = message_text[:-1]                                   # The text of the email message.
    if '"'==message_text[0]:
        message_text = message_text[1:]                                   # The text of the email message.
    print('Creating gmail service')
    service = auth_flow.main(cred_file_dir, script_name)
    print('message text = ',message_text)
    message = CreateMessageWithAttachments(sender, to, cc,subject, message_text, filepath,filenames, html)

    print('Sender: ',sender,'\nReceiver: ',to)
    if cc != None:
        print('cc: ',cc)
    print('sending mail')
    try:
        SendMessage(service, "me", message)     # "me" is the user_id of sender
        print('mail sent')

    except Exception as e:
        print('Exception --> ',e)
        return



if __name__=='__main__':
    # The name of the file/files to be attached.
    file_dir = ''                   # The directory containing the file to be attached.
    main(filepath,filenames)

## How to use this API module
# first import  this module in your main script as follows
# from APIModules.email_module import main as send_mail
# Call this module's main function as follows
# send_mail.main(cred_file_dir,filepath, filenames,SCRIPT_NAME,to, subject, message_text, html = True )
# cred_file_dir is folder path of CREDENTIALS folder
