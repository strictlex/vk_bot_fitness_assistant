import vk_api, random, logging
from config import VK_TOKEN



def send_vk_message(user_id, text):
    try:
        vk_session = vk_api.VkApi(token=VK_TOKEN)
        vk = vk_session.get_api()
        vk.messages.send(
            user_id=user_id,
            message=text,
            random_id=random.randint(1, 2**31)
        )
    except vk_api.ApiError as e:
        logging.error(f"Ошибка VK при отправке {user_id}: {e}")
    except Exception as e:
        logging.error(f"Неизвестная ошибка при отправке {user_id}: {e}")