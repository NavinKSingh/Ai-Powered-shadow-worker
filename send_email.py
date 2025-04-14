import os
import pickle
import base64
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# If modifying the SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

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

def send_email(subject, body, recipient_email):
    """Send an email using the Gmail API."""
    service = build_service()

    # Create the email message
    message = MIMEMultipart()
    message['to'] = recipient_email
    message['from'] = SENDER_EMAIL
    message['subject'] = subject

    # Attach the email body text
    message.attach(MIMEText(body))

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Send the email
    send_message = service.users().messages().send(userId="me", body={'raw': raw_message}).execute()

    print(f'Email sent! Message Id: {send_message["id"]}')

def task_completed_report():
    """Simulate a task completion event and send an email without attachment."""
    # Get user input for recipient email, subject, and body
    recipient_email = input("Enter recipient email: ")
    subject = input("Enter the subject/title of the email: ")
    body = input("Enter the body/content of the email: ")

    # Send email without any attachment
    send_email(subject, body, recipient_email)

if __name__ == '__main__':
    task_completed_report()
