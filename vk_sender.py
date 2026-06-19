import vk_api
from config import VK_TOKEN

def send_vk_message(user_id, text):
        try:
            vk_session = vk_api.VkApi(token=VK_TOKEN)
        except:
            raise Exception("VK токена нет")
        vk = vk_session.get_api()
        vk.messages.send(user_id=user_id, message=text, random_id=0)

