import datetime

def parse_description(events):
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
                    raise Exception("Неверно заполнено описание тренеровки клиента в календаре")
        return event_list