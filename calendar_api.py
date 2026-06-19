import os, pickle, datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from config import SCOPES, SECRET_FILE

def get_token():
    flow = InstalledAppFlow.from_client_secrets_file(SECRET_FILE, scopes=SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

def get_calendar_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if creds is None:
        creds = get_token()
    else:
        if creds.valid:
            pass
        else:
            if creds.refresh_token:
                creds.refresh(Request())
            else:
                creds = get_token()

    with open('token.pickle', 'wb') as token_file:
            pickle.dump(creds, token_file)
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_events(service, time_min=None, time_max=None, max_results=50):
    events_result = service.events().list(calendarId='primary', singleEvents=True, orderBy='startTime').execute()
    return events_result.get('items', [])