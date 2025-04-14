import os
import pickle
import base64
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying the SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# The ID and secret of your OAuth 2.0 Client IDs
CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'gmail'
API_VERSION = 'v1'

# The address of the sender
SENDER_EMAIL = 'ns6419@srmist.edu.in'

def build_service():
    """Build the Gmail API service."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)  # Ensure this matches the redirect URI in your credentials
        # Save the credentials for the next run
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)
    
    return build(API_NAME, API_VERSION, credentials=creds)


def read_emails():
    """Read unread emails using the Gmail API."""
    service = build_service()

    # Call the Gmail API to fetch the latest 10 unread emails
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])

    if not messages:
        print('No unread messages found.')
    else:
        print(f'Found {len(messages)} unread messages:')
        for message in messages[:10]:  # Fetch top 10 unread messages
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = msg['payload']['headers']
            for values in email_data:
                name = values['name']
                if name == 'From':
                    from_name = values['value']
                    print(f'From: {from_name}')
            
            # Decode the email body if it's in plain text
            try:
                if 'parts' in msg['payload']:
                    data = msg['payload']['parts'][0]['body']["data"]
                else:
                    data = msg['payload']['body']["data"]
                byte_code = base64.urlsafe_b64decode(data)
                text = byte_code.decode("utf-8")
                print(f'Body: {text}\n')
            except BaseException as error:
                print(f'An error occurred: {error}')


if __name__ == '__main__':
    read_emails()
