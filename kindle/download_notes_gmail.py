"""
This script was necessary for me because Amazon limits the total of highlights 
you can export both in the My Clippings.txt and in the https://read.amazon.com/notebook.

This way, it seems that I can retrieve all of my notes. 

Status: working as of 08/06/2020.

Author:
    Warley Vital Barbosa
    vitalwarley@gmail.com
"""
import base64
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

creds = None

# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('gmail', 'v1', credentials=creds)
messages_resource = service.users().messages()

results = messages_resource.list(userId='me', q='Notas e destaques criados em seu Kindle').execute()
store_dir = 'notes/'

messages = [service.users().messages().get(userId='me', id=message['id']).execute() for message in results['messages']]

for idx_i, message in enumerate(messages):
    filenames = [part['filename'] for part in message['payload']['parts']]
    for idx_j, fn in enumerate(filenames):
        if not idx_j:
            print()
            continue
        print(f"{idx_i}.{idx_j}: {fn}")

idx = input('\nType desired file id: ')
i, j = [int(_) for _ in idx.split('.')]

part = messages[i]['payload']['parts'][j]
filename = part['filename']
msg_id = messages[i]['id']
att_id = part['body']['attachmentId']
attach_part = messages_resource.attachments().get(id=att_id, userId='me', messageId=msg_id).execute()
file_data = base64.urlsafe_b64decode(attach_part['data'].encode('UTF-8'))

filename = input('Filename: ')
path = ''.join([store_dir, filename])
with open(path, 'wb') as f:
    f.write(file_data)

print("Saved: {path}")
