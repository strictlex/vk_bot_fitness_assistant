import os
from dotenv import load_dotenv


load_dotenv()
VK_TOKEN = os.getenv('VK_TOKEN')
if not VK_TOKEN:
    raise ValueError("VK_TOKEN не задан в .env")
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SECRET_FILE = 'credentials.json'
TIMEZONE_OFFSET = int(os.getenv('TIMEZONE_OFFSET', 4))
TRAINER_VK_ID = int(os.getenv('TRAINER_VK_ID', 15705227))
GROUP_ID = int(os.getenv('GROUP_ID', 239622096))
