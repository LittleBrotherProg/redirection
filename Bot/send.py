from vkbottle import User, PhotoMessageUploader, VKAPIError, DocMessagesUploader
from aiogram import Bot
import requests
import os
from io import BytesIO
bot_vk = User(os.getenv("USERVK"))
bot_tg = Bot(os.getenv("USERTG"))

photo_uploader = PhotoMessageUploader(bot_vk.api)
document_uploader = DocMessagesUploader(bot_vk.api)

# id страницы в ВК человека от которого хотим принимать сообщения
peer_id = os.getenv("KATEVK")
async def send_messages_vk(text, random_id):
    await bot_vk.api.messages.send(message = text, random_id=random_id, peer_id=peer_id)

async def send_messages_tg(text):
    await bot_tg.send_message(os.getenv("METG"), text)

async def send_photo_vk(url, random_id):
    img = requests.get(url).content
    f = BytesIO(img)
    try:
        photo = await photo_uploader.upload(
                                            file_source=f,
                                            peer_id=peer_id
                                            )
        await bot_vk.api.messages.send(attachment=photo, random_id=random_id, peer_id=peer_id)
    except VKAPIError as error:
        print(f"Error uploading photo: {error}")


async def send_document_vk(url, random_id, name_file):
    document = requests.get(url).content
    docbit = BytesIO(document)
    try:
        doc = await document_uploader.upload(
                                            file_source=docbit,
                                            peer_id=peer_id,
                                            title = name_file
                                            )
        await bot_vk.api.messages.send(attachment=doc, random_id=random_id, peer_id=peer_id)
    except VKAPIError as error:
        print(f"Error uploading photo: {error}")