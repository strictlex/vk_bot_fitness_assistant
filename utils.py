from config import TIMEZONE_OFFSET
from datetime import datetime, timedelta, timezone


MONTHS_RU = {
    'January': 'января',
    'February': 'февраля',
    'March': 'марта',
    'April': 'апреля',
    'May': 'мая',
    'June': 'июня',
    'July': 'июля',
    'August': 'августа',
    'September': 'сентября',
    'October': 'октября',
    'November': 'ноября',
    'December': 'декабря'
}

def get_tomorrow_date(offset_hours):
    tz = timezone(timedelta(hours=offset_hours))
    now = datetime.now(tz)
    return (now+timedelta(days=1)).date()



