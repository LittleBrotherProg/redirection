import vk_api
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
import telebot
import requests
# import json
import datetime
from threading import Thread
from YA import *
from io import BytesIO

# Класс отвечающий за работу с ВК

class VK:

    # Функция ицилизации 
    def __init__(self):
        # Требуется токен ПОЛУЧЯТЕЛЯ сообщений
        self.token = open('token_vk.txt').read()
        # Авторизация в ВК
        self.vk_session = vk_api.VkApi(token= self.token)
        # Сохранения текущей сессии
        self.vk = self.vk_session.get_api()
        self.peer_id = 146246943
        self.upload = VkUpload(self.vk)
        self.params = {
                    'access_token': self.token, 
                    'v': '5.131'
                    }

    # Функция для поиски новых сообщений от конкретного пользователя
    def catch_messages(self):
        longpoll = VkLongPoll(self.vk_session)
        for event in longpoll.listen():
            # Ловим новое сообщение и проверяем от кого оно
            if event.type == VkEventType.MESSAGE_NEW and event.user_id == 146246943 and  event.to_me:
                if event.attachments['attach1_type'] == 'photo':
                    pass
                    # id_profile_picture = event.attachments['attach1']
                    # url = 'https://api.vk.com/method/photos.get'
                    # params= {
                    #             'owner_id': 422264572, 
                    #             'photo_ids': id_profile_picture,
                    #             'extended': '1'
                    #             }
                    # info_photo = requests.get(
                    #                             url, 
                    #                             params={
                    #                                     **self.params, 
                    #                                     **params
                    #                                     }
                    #                             )
                    # bot.send_message(1052739314, i['photo']['sizes'][-1]['url'])

                # Вытаскиваем текст нужного нам сообщения и помешаем в переменную  
                # user = self.vk_session.method("users.get", 
                #                               {"user_ids": event.user_id}
                #                               )
                # full_name = user[0]['first_name'] + ' ' + user[0]['last_name']
                # message_for_tg = event.text
                # # Пеобразование времени отправки сообщения в читаемое
                # value = datetime.datetime.fromtimestamp(event.timestamp)
                # time = value.strftime('%Y-%m-%d %H:%M:%S')
                # # Выводим в консоль дату и и время, от кого сообщение и текст сообщения
                # print('=' * 20,
                #       '\n',
                #       f'Дата и время отправки: {time}\n',
                #       f'Сообщение от: {full_name}\n', 
                #       f'Текст сообщения: {message_for_tg}',
                #     )
                # # Инцилизируем класс отвечающий за работу с Телеграммом
                # tg = TG()
                # # Активирцем функцию для отправки сообщения в Телеграмм
                # status = tg.accept_message(message_for_tg)
                # # Выводим в консоль статус кода и расшифровку
                # print(f'Код запроспа на отправку сообщения в тг: {status[0]}',
                #       '\n',
                #       f'Расшифровка кода запроса: {status[1]} \n',
                #       '=' * 20        
                #       )
    # Функция отправки сообщения из Телеграмма в Вк
    def accept_message_text(self, message_tg, random_id):
        # Отправка сообщения
        self.vk.messages.send(user_id=146246943,random_id = random_id, message=message_tg)
        print('Отправка успешна',
              '=' * 20)
    
    def upload_photo(self, url):
        img = requests.get(url).content
        f = BytesIO(img)

        response = self.upload.photo_messages(f)[0]

        owner_id = response['owner_id']
        photo_id = response['id']
        access_key = response['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        self.vk.messages.send(
            random_id=get_random_id(),
            peer_id=self.peer_id,
            attachment=attachment
        )
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
        # id пользователя которуму будем адресовать сообщения
        self.chat_id = '2134234148'
        # Ловим сообщения которые пишем боту
        @self.bot.message_handler(content_types=['text'])
        def catch_text(chat_id,message):
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
                vk.accept_message_text(message_for_vk, random_id)
        @self.bot.message_handler(content_types=['photo'])
        def catch_photo(message):
            file = self.bot.get_file(message.photo[-1].file_id)
            # file_info = self.bot.get_file(file_id)
            # downloaded_file = self.bot.download_file(file_info.file_path)
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

            # with open(r'C:\Users\Kaplin\Desktop\photo_tg\lol.png','wb') as H:
            #     H.write(downloaded_file)


                
                

    def run(self):
        self.bot.polling()

    # Функция отправки сообщения от бота к пользователю
    def accept_message(self, message_vk):
        # Сборка url для отправки запроса на отправку сообщения
        url = self.url + self.token + '/sendMessage'
        accept = requests.post(url, data={ 
                                    'chat_id': self.chat_id,
                                    'text': message_vk
                                    })
        if accept.status_code != 200:
            return [accept.status_code,
                    accept.json()['description']
                    ]
        else:
            return [accept.status_code,
                    accept.reason
                    ]


# Запуск программы
if __name__ == '__main__':
    # Инцилизация класса VK
    vk = VK()
    # Инцилизация класса TG
    tg = TG()   
    Thread(target = lambda: tg.run()).start()
    Thread(target = lambda: vk.catch_messages()).start()