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
store_dir = ''

for message in results['messages']:
    msg_id = message['id']
    message = service.users().messages().get(userId='me', id=msg_id).execute()
    for part in message['payload']['parts']:
        if part['filename']:
            mimetype = part['mimeType']
            if mimetype == 'text/csv':
                filename = part['filename']
                att_id = part['body']['attachmentId']
                attach_part = messages_resource.attachments().get(id=att_id, userId='me', messageId=msg_id).execute()
                file_data = base64.urlsafe_b64decode(attach_part['data'].encode('UTF-8'))
                path = ''.join([store_dir, part['filename']])
                with open(path, 'wb') as f:
                    f.write(file_data)
