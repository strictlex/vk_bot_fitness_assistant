import datetime, vk_sender

def parse_description(events):
        event_list =[]
        for event in events:
            client = []
            try:
                summary = event.get('summary')
                description = event.get('description')
                if not description or description.split('\n')[0].lower() != 'тренировка':
                    continue
                elif description.split('\n')[0].lower() == 'тренировка':
                    check_lines = description.split('\n')
                    if len(check_lines) // 2 == 0:
                        text = f'В описании тренировок на завтра есть нестыковки. Если ты получила это сообщение, то исправь и уведоми клиента сама'
                        vk_sender.send_vk_message(8011518,text)
                        raise ValueError("В описании должно быть две строки: тренировка, имя и VK ID")
                    elif len(check_lines) // 2 != 0 and len(check_lines) >2:
                        lines = iter(check_lines)
                        next(lines)
                        while True:
                            try:
                                name = next(lines).strip()
                                vk_id = int(next(lines).strip())
                                start = event.get('start', {})
                                start_time = start.get('dateTime')
                                if not start_time:
                                    start_time = start.get('date')
                                if not start_time:
                                    raise ValueError("Не удалось получить дату/время события")
                                client = [summary, name, vk_id, start_time]
                                event_list.append(client)
                            except StopIteration:
                                break
            except (KeyError, ValueError, IndexError) as e:
                raise Exception(f"Ошибка в событии '{summary}': {e}")
            
        return event_list