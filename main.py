import vk_api
import telebot
import requests
from vk_api.longpoll import VkLongPoll, VkEventType

class vk:
    
    def __init__(self, message_tg):
        self.message = message_tg
        self.token = open('token_vk.txt').read()
        self.vk_session = vk_api.VkApi(token= self.token)
        self.tg = self.vk_session.get_api()

    def catch_messages(self):
        longpoll = VkLongPoll(self.vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.user_id == 146246943:
                message_for_tg = event.text
                tg = TG(message_for_tg)
                tg.accept_message()
                print('accept')
    
    def accept_message(self):
        self.tg.message.send(user_id=146246943, message=self.message)



                


class TG:

    def __init__(self, message_vk):
        self.token = open('token_tg.txt').read()
        self.bot = telebot.TeleBot(self.token, parse_mode=None)
        self.message = message_vk
        self.url = 'https://api.telegram.org/bot'
        self.chat_id = '2134234148'
        @self.bot.message_handler()
        def catch_text(message):
            if(message.text != ''):
                message_for_vk = message.text
                VK = vk(message_for_vk)
                send_message = VK.accept_message()
                

    def run(self):
        self.bot.polling()

    def accept_message(self):
        url = self.url + self.token + '/sendMessage'
        r = requests.post(url, data={ 
                                    'chat_id': self.chat_id,
                                    'text': self.message
                                    })
        print(r.status_code)
    


if __name__ == '__main__':
    tg = TG('l')
    tg.run()