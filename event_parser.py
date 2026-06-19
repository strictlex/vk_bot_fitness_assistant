import datetime

def parse_description(events):
        event_list =[]
        for event in events:
            client = []
            try:
                summary = event.get('summary')
                if not summary or summary.lower() != 'тренеровка':
                    continue
                description = event.get('description')
                if not description:
                    raise ValueError("Отсутствует описание события")
                lines = description.split('\n')
                if len(lines) < 2:
                    raise ValueError("В описании должно быть две строки: имя и VK ID")
                name = lines[0].strip()
                vk_id = int(lines[1].strip())
                start = event.get('start', {})
                start_time = start.get('dateTime')
                if not start_time:
                    start_time = start.get('date')
                if not start_time:
                    raise ValueError("Не удалось получить дату/время события")
                client = [summary, name, vk_id, start_time]
                event_list.append(client)
            except (KeyError, ValueError, IndexError) as e:
                raise Exception(f"Ошибка в событии '{summary}': {e}")
            
        return event_list