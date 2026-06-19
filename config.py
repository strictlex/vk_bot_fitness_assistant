import os
from dotenv import load_dotenv


load_dotenv()
VK_TOKEN = os.getenv('VK_TOKEN')
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SECRET_FILE = 'credentials.json'
TIMEZONE_OFFSET = 4