import vk_api
import telebot
import requests
# import json
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from threading import Thread

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

    # Функция для поиски новых сообщений от конкретного пользователя
    def catch_messages(self):
        longpoll = VkLongPoll(self.vk_session)
        for event in longpoll.listen():
            # Ловим новое сообщение и проверяем от кого оно
            if event.type == VkEventType.MESSAGE_NEW and event.user_id == 146246943:
                # Вытаскиваем текст нужного нам сообщения и помешаем в переменную  
                user = self.vk_session.method("users.get", 
                                              {"user_ids": event.user_id}
                                              )
                full_name = user[0]['first_name'] + ' ' + user[0]['last_name']
                message_for_tg = event.text
                # Пеобразование времени отправки сообщения в читаемое
                value = datetime.datetime.fromtimestamp(event.timestamp)
                time = value.strftime('%Y-%m-%d %H:%M:%S')
                # Выводим в консоль дату и и время, от кого сообщение и текст сообщения
                print('=' * 20,
                      '\n',
                      f'Дата и время отправки: {time}\n',
                      f'Сообщение от: {full_name}\n', 
                      f'Текст сообщения: {message_for_tg}',
                    )
                # Инцилизируем класс отвечающий за работу с Телеграммом
                tg = TG()
                # Активирцем функцию для отправки сообщения в Телеграмм
                status = tg.accept_message(message_for_tg)
                # Выводим в консоль статус кода и расшифровку
                print(f'Код запроспа на отправку сообщения в тг: {status[0]}',
                      '\n',
                      f'Расшифровка кода запроса: {status[1]} \n',
                      '=' * 20        
                      )
    
    def accept_message(self, message_tg, random_id):
        print('message accept in vk')
        self.vk.messages.send(user_id=146246943,random_id = random_id, message=message_tg)


class TG:

    def __init__(self):
        self.token = open('token_tg.txt').read()
        self.bot = telebot.TeleBot(self.token, parse_mode=None)
        self.url = 'https://api.telegram.org/bot'
        self.chat_id = '2134234148'
        @self.bot.message_handler()
        def catch_text(message):
            if(message.text != ''):
                message_for_vk = message.text
                vk = VK()
                random_id = message.id
                send_message = vk.accept_message(message_for_vk, random_id)
                print('accept')
                

    def run(self):
        self.bot.polling()

    def accept_message(self, message_vk):
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

        


if __name__ == '__main__':
    vk = VK()
    tg = TG()   
    Thread(target = lambda: tg.run()).start()
    Thread(target = lambda: vk.catch_messages()).start()