import datetime, config, calendar_api, event_parser, vk_sender, utils

service = calendar_api.get_calendar_service()
events = calendar_api.get_events(service)
events_list = event_parser.parse_description(events)
tommorow = utils.get_tomorrow_date(config.TIMEZONE_OFFSET)


for client in events_list:
    date = datetime.datetime.fromisoformat(client[3]).date()
    if date == tommorow:
        name = client[1].split()[1]
        date_time_iso = datetime.datetime.fromisoformat(client[3])
        day = date_time_iso.strftime("%d")
        name_month = utils.MONTHS_RU[date_time_iso.strftime("%B")]
        time_day = date_time_iso.strftime("%H:%M")
        text = f'{name}, привет! Завтра, {day} {name_month} в {time_day}, жду тебя на тренеровку. Если не получается напиши мне @lanaterenteva'

        vk_sender.send_vk_message(client[-1],text)
