import os
import pickle
import google.auth
from google.auth.transport.requests import Request 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scopes required for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Path to your credentials.json file
CLIENT_SECRET_FILE = 'credentials.json'

# Token file to store user credentials after authentication
TOKEN_FILE = 'token.pickle'

def get_credentials():
    """Gets valid user credentials from storage or initiates OAuth flow."""
    credentials = None

    # Check if the token file exists
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            credentials = pickle.load(token)

    # If no valid credentials are available, prompt for authentication
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            credentials = flow.run_local_server(port=8080)

        # Save the credentials for the next run
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(credentials, token)

    return credentials

def build_service():
    """Builds the Gmail API service."""
    credentials = get_credentials()
    service = build('gmail', 'v1', credentials=credentials)
    return service
