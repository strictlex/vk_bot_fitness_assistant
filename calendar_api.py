import os, pickle, datetime,logging
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

    if creds and creds.valid:
        pass
    elif creds and creds.refresh_token:
        creds.refresh(Request())
    else:
        creds = get_token()

    with open('token.pickle', 'wb') as token_file:
            try:
                pickle.dump(creds, token_file)
            except Exception as e:
                logging.error(f"Не удалось сохранить token.pickle: {e}")
            
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_events(service,now):
    event_result = service.events().list(calendarId='primary',
                                         singleEvents=True,
                                         orderBy='startTime',
                                         timeMin = now).execute()
    events = event_result.get('items',[])
    return events

