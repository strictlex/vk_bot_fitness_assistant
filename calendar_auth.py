from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os, pickle, datetime, vk_api, locale
from datetime import timezone
from dotenv import load_dotenv

load_dotenv()

try:
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
except:
    pass
VK_TOKEN = os.getenv('VK_TOKEN')

def main():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    secret_file  = 'credentials.json'


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

    def get_token():
        flow = InstalledAppFlow.from_client_secrets_file(secret_file, scopes=SCOPES)
        creds = flow.run_local_server(port=0)
        return creds
    
    def parse_description(events:list)-> list[list]:
        event_list =[]
        for event in events:
            client = []
            if event.get('summary').lower() == 'тренеровка':
                try:
                    client.append(event.get('summary'))
                    description = event.get('description').split("\n")
                    client.append(description[0])
                    client.append(int(description[1]))
                    start_time = event.get('start').get("dateTime")
                    client.append(start_time)
                    event_list.append(client)
                except: 
                    raise Exception("Неверно заполнено описание клиента")
        return event_list

    def send_vk_message(*args):
        _, fio, vk_id, date_time = args
        name = fio.split()[1]
        vk_session = vk_api.VkApi(token=VK_TOKEN)
        vk = vk_session.get_api()
        date_time_iso = datetime.datetime.fromisoformat(date_time)
        weekday = date_time_iso.strftime("%A")
        day_month = date_time_iso.strftime("%d %B")
        time_day = date_time_iso.strftime("%H:%M")
        vk.messages.send(user_id=int(vk_id),message = f'{name}, привет! Завтра, {day_month} в {time_day}, жду тебя на тренеровку. Если не получается напиши мне @lanaterenteva',random_id=0)


    tz = datetime.timezone(datetime.timedelta(hours=4))
    now_locale = datetime.datetime.now(tz)
    tommorow_date = (now_locale+datetime.timedelta(days=1)).date()
    service = get_calendar_service()
    event_result = service.events().list(calendarId='primary',
                                         singleEvents=True,
                                         orderBy='startTime',
                                         timeMin = now_locale.isoformat()).execute()

    events = event_result.get('items',[])
    event_list = parse_description(events)

    if event_list:
        for client in event_list:
            data = datetime.datetime.fromisoformat(client[3]).date()
            if data == tommorow_date:
                send_vk_message(*client)
                print(f'Сообщение отправлено {client[1]} ')
   
if __name__ == '__main__':
    main()