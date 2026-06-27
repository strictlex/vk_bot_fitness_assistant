import logging
import config
import vk_api
import json
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(file):
    try:
        logging.info("Загрузка списка клиентов")
        with open(file,'r',encoding='utf-8') as f:
            clients = json.load(f)
        logging.info(f"Загружено {len(clients)} клиентов")

        logging.info("Авторизация VK...")
        vk_session = vk_api.VkApi(token=config.VK_TOKEN)
        vk = vk_session.get_api()
        logging.info("VK авторизация успешна")

        logging.info("Создание LongPoll...")
        longpoll = VkBotLongPoll(vk_session,config.GROUP_ID)
        logging.info(f"LongPoll запущен для группы {config.GROUP_ID}. Ожидание сообщений...")

        for event in longpoll.listen():
            try:
                if event.type == VkBotEventType.MESSAGE_NEW:
                        from_id = event.obj.message['from_id']   # type: ignore
                        text = event.obj.message['text']           # type: ignore
                        logging.info(f"Получено сообщение от {from_id}: {text}")

                        if from_id == config.TRAINER_VK_ID:
                            logging.info("Сообщение от тренера, игнорируем")
                            continue

                        found = False
                        for name, vk_id in clients.items():
                            if vk_id == from_id:
                                vk.messages.send(
                                    user_id=config.TRAINER_VK_ID,
                                    message=f"От клиента {name}(vk.com/id{from_id}):)",
                                    random_id=get_random_id()
                                    )
                                forward_data = {
                                    'peer_id': from_id,
                                    'message_ids': [event.obj.message['id']]
                                }
                                forward_json = json.dumps(forward_data, ensure_ascii=False)
                                vk.messages.send(
                                    user_id=config.TRAINER_VK_ID,
                                    random_id=get_random_id(),
                                    forward=forward_json
                                )
                                logging.info(f"Переслано сообщение от клиента {name} тренеру")
                                found = True
                                break
                        if not found:
                             logging.info(f"Сообщение от пользователя {from_id}, игнорируем")
            except Exception as e:
                logging.error(f"Ошибка при обработке события: {e}", exc_info=True)

    except Exception as e:
        logging.critical(f"Критическая ошибка в listener: {e}", exc_info=True)
        raise

if __name__ == '__main__':
    main('clients.json')