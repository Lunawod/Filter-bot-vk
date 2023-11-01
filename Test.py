import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from pymongo import MongoClient

banned_words = ["bad", "evil", "hate"]

def send_warning(vk, user_id):
    vk.messages.send(
        user_id=user_id,
        message="Ваше сообщение содержит запрещенное слово. Пожалуйста, переформулируйте его.",
        random_id=0
    )

def check_message(message):
    for word in banned_words:
        if word in message.lower():
            return True
    return False

def handle_new_message(event, vk, db):
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        message = event.text
        user_id = event.user_id
        if check_message(message):
            send_warning(vk, user_id)
        db.users.insert_one({"user_id": user_id, "message": message})

vk_session = vk_api.VkApi(token='Token')
vk = vk_session.get_api()


client = MongoClient('Link')
db = client['Mydatabase']


longpoll = VkLongPoll(vk_session)


for event in longpoll.listen():
    handle_new_message(event, vk, db)
