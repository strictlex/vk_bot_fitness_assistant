from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

"""Файл использовать только в случае просрочки token.pickle"""



SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SECRET_FILE = 'credentials.json'

flow = InstalledAppFlow.from_client_secrets_file(SECRET_FILE, scopes=SCOPES)
creds = flow.run_local_server(port=0)

with open('token.pickle', 'wb') as f:
    pickle.dump(creds, f)

print("✅ token.pickle успешно создан")