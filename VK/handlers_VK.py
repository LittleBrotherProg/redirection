import time
import os
import requests
from Bot.YA import  YA
from vkbottle import User
from vkbottle.user import Message, rules
from Bot.send import send_messages_tg, send_photo_tg, send_doc_tg


bot = User(os.getenv("USERVK"))
peer_id = os.getenv("KATEVK")

@bot.on.private_message(rules.AttachmentTypeRule('audio_message'))
async def audio_message(ms: Message):
    if ms.attachments[0].audio_message.transcript_state == 'in_progress':
        time.sleep(5)
        params = {
            "access_token": os.getenv('USERVK'),
            "message_ids": ms.id,
            "v": '5.131'
        }
        result = requests.get(
                              f'https://api.vk.com/method/messages.getById?', 
                              params={**params}
                              ).json()
        text_audio = result['response']['items'][0]['attachments'][0]['audio_message']['transcript']
        await send_messages_tg(text_audio)
    else:
        text_audio = ms.attachments[0].audio_message.transcript
        await send_messages_tg(text_audio)

@bot.on.private_message(rules.AttachmentTypeRule('photo'))
async def photo(ms: Message):
        info_photo = ms.attachments[0].photo.sizes[-5]
        ya = YA(
                info_photo.url,  
                str(info_photo.height * info_photo.width) + '.jpg', 
                info_photo.height * info_photo.width
                )
        ya.create_folder()
        ya.loading_profile_picture()
        dowland_url = ya.dowland_photo()
        await send_photo_tg(dowland_url)

@bot.on.private_message(rules.AttachmentTypeRule('doc'))
async def doc(ms: Message):
        info_photo = ms.attachments[0].doc
        ya = YA(
                info_photo.url,  
                str(info_photo.title), 
                info_photo.size
                )
        ya.create_folder()
        ya.loading_profile_picture()
        dowland_url = ya.dowland_photo()
        await send_doc_tg(dowland_url)



@bot.on.private_message()
async def catching_message(ms: Message):
    if ms.peer_id == int(peer_id):
        await send_messages_tg(ms.text)


    

