import os
from dotenv import load_dotenv


load_dotenv()
VK_TOKEN = os.getenv('VK_TOKEN')
if not VK_TOKEN:
    raise ValueError("VK_TOKEN не задан в .env")
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SECRET_FILE = 'credentials.json'

timzone_offset = os.getenv('TIMEZONE_OFFSET')
if not timzone_offset:
    raise ValueError("TIMEZONE_OFFSET не задан в .env")
TIMEZONE_OFFSET = int(timzone_offset)

trainer_vk = os.getenv('TRAINER_VK_ID')
if not trainer_vk:
    raise ValueError("TRAINER_VK_ID не задан в .env")
TRAINER_VK_ID = int(trainer_vk)

group_id = os.getenv('GROUP_ID')
if not group_id:
    raise ValueError("GROUP_ID не задан в .env")
GROUP_ID = int(group_id)

