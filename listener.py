import logging,config, vk_api, vk_api.bot_longpoll, vk_api.utils,json, vk_sender
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.utils import get_random_id
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(file):
    try:
        with open(file,'r',encoding='utf-8') as f:
                clients = json.load(f)
        
        vk_session = vk_api.VkApi(token=config.VK_TOKEN)
        vk = vk_session.get_api()

        longpoll = vk_api.bot_longpoll.VkBotLongPoll(vk_session,config.GROUP_ID)

        while True:
            try:
                 for event in longpoll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW:
                         from_id = event.obj.message['from_id']   # type: ignore
                         if from_id == config.TRAINER_VK_ID:
                              continue
                         text = event.obj.message['text']           # type: ignore
                         for name, vk_id in clients.items():
                              if vk_id == from_id:
                                    vk.messages.send(
                                        user_id=config.TRAINER_VK_ID,
                                        message=f"От клиента {name}: {text}",
                                        random_id=get_random_id()
                                        )
                                    logging.info(f'Ошибки')
            except Exception as e:
                logging.error(f"Ошибка в listener: {e}")
    except Exception as e:
                logging.error(f"Ошибка в listener: {e}")