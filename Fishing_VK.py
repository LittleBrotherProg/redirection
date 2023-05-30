from vkbottle.user import User, Message
import asyncio
from io import BytesIO


class VK:

    # Функция ицилизации 
    def __init__(self):
        # В файл token_vk.txt нужно поместить токен пользователя ВК.
        # Токен должен обладать параметрами: доступ в любое время, доступ к сообщениям.
        self.bot = User(open('token_vk.txt').read())
        # id страницы в ВК человека от которого хотим принимать сообщения
        self.peer_id = 146246943
        # обработчик входящих сообщений
        @self.bot.on.message()
        async def chatting(message: Message):
            if message.from_id == 146246943:
                transit_tg = transit()
                message_vk = message.text
                transit_tg.accept_forward_text(message_vk, 'tg', 0)
    # Функция приёма и отправки сообщения из ТГ
    async def accept_message(self, message_for_vk, random_id):
          await  self.bot.api.messages.send(peer_id=self.peer_id, message=message_for_vk, random_id=random_id)  
    # Запуск обработки сообщений
    def fishing_start(self):
        self.bot.run_forever()

    
    