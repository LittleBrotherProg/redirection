import telebot
import requests
import asyncio
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

        @self.bot.message_handler(commands=['start'])
        def greeting(message):
            self.bot.send_message(message.chat.id, "Доброго времени суток.")

        @self.bot.message_handler(content_types=['text'])
        def catch_text(message):
            if(message.text != ''):
                message_for_vk = message.text
                random_id = message.id
                print('=' * 20,
                      '\n',
                      f'Время отправки \n',
                      f'Сообщение от: {message.from_user.full_name} из ТГ \n',
                      f'Текст сообщения: {message.text}',
                      )
                # Отправляем написанное сообщение в ВК
                accept_forward_text(message_for_vk, 'vk', random_id)
    
    def fishing_start(self):
        self.bot.polling()

    def accept_message(self, message_vk):
        url = self.url + self.token + '/sendMessage'
        accept = requests.post(url, data={ 
                                    'chat_id': self.chat_id,
                                    'text': message_vk
                                    })

        # @self.bot.message_handler(content_types=['photo'])
        # def catch_photo(message):
        #     file = self.bot.get_file(message.photo[-1].file_id)
        #     url = f'https://api.telegram.org/file/bot{self.token}/{file.file_path}'
        #     # load_photo = YA( 
        #     #         url,  
        #     #         str(message.photo[-1].file_unique_id), 
        #     #         message.photo[-1].file_size
        #     #         )
        #     # load_photo.create_folder()
        #     # load_photo.loading_profile_picture()
        #     # dowland_url = load_photo.dowland_photo()
        #     # vk = VK()
        #     # vk.upload_photo(dowland_url)

        # @self.bot.message_handler(content_types=['document'])
        # def catch_photo(message):
        #     file = self.bot.get_file(message.document.file_id)
        #     # file_info = self.bot.get_file(file_id)
        #     # downloaded_file = self.bot.download_file(file_info.file_path)
        #     url = f'https://api.telegram.org/file/bot{self.token}/{file.file_path}'
        #     load_photo = YA( 
        #             url,  
        #             str(message.document.file_name), 
        #             message.document.file_size
        #             )
        #     load_photo.create_folder()
        #     load_photo.loading_profile_picture()
        #     dowland_url = load_photo.dowland_document()
            # Отправка ссылки для отправки в фото в ВК ТРЕБУЕТ ПЕРЕРАБОТКИ
            # vk = VK()
            # vk.upload_photo(dowland_url)

        # if accept.status_code != 200:
        #     return [accept.status_code,
        #             accept.json()['description']
        #             ]
        # else:
        #     return [accept.status_code,
        #             accept.reason
        #             ]
