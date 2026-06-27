import datetime, config, calendar_api, event_parser, vk_sender, utils,logging
from datetime import datetime, timezone, timedelta
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

now = utils.get_tomorrow_date(config.TIMEZONE_OFFSET)[1].isoformat()
tomorrow = utils.get_tomorrow_date(config.TIMEZONE_OFFSET)[0]

service = calendar_api.get_calendar_service()
events = calendar_api.get_events(service,now)
events_list = event_parser.parse_description(events)

logging.info(f"Найдено событий: {len(events_list)}")
for c in events_list:
    logging.info(f"Событие: {c[1]}, время: {c[3]}")





for client in events_list:
    try:
        event_date = datetime.fromisoformat(client[3]).date()
        logging.info(f"Дата события: {event_date}, завтра: {tomorrow}")
        if event_date != tomorrow:
            logging.info(f"Пропускаем событие {client[1]}, дата не совпадает")
            continue

        name_parts = client[1].split()
        if len(name_parts) < 2:
            logging.warning(f"Неполное имя у клиента {client[1]}, используется имя как есть")
            name = client[1]
        else:
            name = name_parts[1]

        date_time_iso = datetime.fromisoformat(client[3])
        day = date_time_iso.strftime("%d")
        name_month = utils.MONTHS_RU[date_time_iso.strftime("%B")]
        time_day = date_time_iso.strftime("%H:%M")
        text = f'{name}, привет! Завтра, {day} {name_month} в {time_day}, жду тебя на тренировку. Если не получается напиши мне @lanaterenteva'

        vk_sender.send_vk_message(client[2], text)
        logging.info(f"Отправлено {name}")
    except Exception as e:
        logging.error(f"Ошибка при обработке клиента {client}: {e}")

