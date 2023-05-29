
from vkbottle.user import User, Message
import random
import telebot
import requests
# import json
import datetime
from multiprocessing import Process
from YA import *
from io import BytesIO
import asyncio


# Класс отвечающий за работу с ВК

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
                tg = TG()
                message_vk = message.text
                tg.accept_message(message_vk)
    # Функция приёма и отправки сообщения из ТГ
    async def accept_message_text(self, message_for_vk, random_id):
          await  self.bot.api.messages.send(peer_id=self.peer_id, message=message_for_vk, random_id=random_id)  
    # Запуск обработки сообщений
    def work_start(self):
        self.bot.run_forever()

    
    
# Класс отвечающий за работу с Телеграмом

class TG:

# Функция ицилизации 
    def __init__(self):
        # Требуется токен БОТА сообщений
        self.token = open('token_tg.txt').read()
        # Авторизация бота в Телеграмме
        self.bot = telebot.TeleBot(self.token, parse_mode=None)
        # Ссылка для работы с api Телеграмма
        self.url = 'https://api.telegram.org/bot'
        # id пользователя ТГ который будет принимать сообщения
        self.chat_id = '2134234148'
        # Ловим сообщения которые пишем боту
        @self.bot.message_handler(content_types=['text'])
        def catch_text(message):
            if(message.text != ''):
                message_for_vk = message.text
                vk = VK()
                random_id = message.id
                print('=' * 20,
                      '\n',
                      f'Время отправки \n',
                      f'Сообщение от: {message.from_user.full_name} из ТГ \n',
                      f'Текст сообщения: {message.text}',
                      )
                # Отправляем написанное сообщение в ВК
                asyncio.run(vk.accept_message_text(message_for_vk, random_id))

        @self.bot.message_handler(content_types=['photo'])
        def catch_photo(message):
            file = self.bot.get_file(message.photo[-1].file_id)
            url = f'https://api.telegram.org/file/bot{self.token}/{file.file_path}'
            load_photo = YA( 
                    url,  
                    str(message.photo[-1].file_unique_id), 
                    message.photo[-1].file_size
                    )
            load_photo.create_folder()
            load_photo.loading_profile_picture()
            dowland_url = load_photo.dowland_photo()
            vk = VK()
            vk.upload_photo(dowland_url)

        @self.bot.message_handler(content_types=['document'])
        def catch_photo(message):
            file = self.bot.get_file(message.document.file_id)
            # file_info = self.bot.get_file(file_id)
            # downloaded_file = self.bot.download_file(file_info.file_path)
            url = f'https://api.telegram.org/file/bot{self.token}/{file.file_path}'
            load_photo = YA( 
                    url,  
                    str(message.document.file_name), 
                    message.document.file_size
                    )
            load_photo.create_folder()
            load_photo.loading_profile_picture()
            dowland_url = load_photo.dowland_document()
            # Отправка ссылки для отправки в фото в ВК ТРЕБУЕТ ПЕРЕРАБОТКИ
            # vk = VK()
            # vk.upload_photo(dowland_url)
      
    def run(self):
        self.bot.polling()

    # Функция принимает и  отправляет полученые сообщения из ВК от бота к пользователю
    def accept_message(self, message_vk):
        # Сборка url для отправки запроса на отправку сообщения
        url = self.url + self.token + '/sendMessage'
        accept = requests.post(url, data={ 
                                    'chat_id': self.chat_id,
                                    'text': message_vk
                                    })
        # if accept.status_code != 200:
        #     return [accept.status_code,
        #             accept.json()['description']
        #             ]
        # else:
        #     return [accept.status_code,
        #             accept.reason
        #             ]

def start_vk():
    vk = VK()
    vk.work_start()

def start_tg():
    tg = TG()
    tg.run()

# Запуск программы
if __name__ == '__main__':
    g1 = Process(target=start_vk)
    g2 = Process(target=start_tg)
    g1.start()
    g2.start()
    g1.join()
    g2.join()