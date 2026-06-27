import json, vk_sender, config, logging, os
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main(file):
    try:

        with open(file,'r',encoding='utf-8') as f:
            clients = json.load(f)
            logging.info('Загружает клиентов')

        for name, vk_id in clients.items():
            name = name.split()[1]
            text = f'Привет, {name}! Отправь пожалуйста как ты сегодня питалась.'
            vk_sender.send_vk_message(vk_id, text)
            logging.info(f"Отправлен запрос отчёта клиенту {name} (ID {vk_id})")
    except Exception as e:
        logging.error(f"Ошибка в send_dinner: {e}", exc_info=True)




if __name__ == '__main__':
    main("clients.json")