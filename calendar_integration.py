import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# The SCOPES needed to access Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

# The path to your credentials.json file
CLIENT_SECRET_FILE = 'credentials.json'

# The redirect URI to use (ensure this matches the one in Google Cloud Console)
REDIRECT_URI = 'http://localhost:8080/'

def get_credentials():
    """Gets valid user credentials from storage or initiates the OAuth2.0 flow."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def create_event():
    """Creates an event on the user's Google Calendar."""
    creds = get_credentials()

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': 'Meeting with Team',
        'location': 'Online',
        'description': 'Discussing the next steps of the project.',
        'start': {
            'dateTime': '2025-03-15T09:00:00-07:00',  # Example date and time
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2025-03-15T10:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'attendees': [
            {'email': 'team@example.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    try:
        event_result = service.events().insert(
            calendarId='primary', body=event).execute()
        print(f"Event created: {event_result.get('htmlLink')}")
    except Exception as error:
        print(f"An error occurred: {error}")

if __name__ == '__main__':
    create_event()
