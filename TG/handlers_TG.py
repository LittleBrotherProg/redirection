from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import Command
from Bot.send import send_messages_vk, send_photo_vk, send_document_vk
from Bot.YA import YA 
import os

router = Router()
bot = Bot(os.getenv("USERTG"))

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(f"{msg.chat.first_name} бот переадресат предназначеня для отправки сообщений из телеграмм в социальную сеть Вконтакте, так и для принятия сообщений из Вконтакте и отправки Вам")

@router.message(F.photo)
async def get_photo(msg: Message):
    info_photo = msg.photo[-1]
    file = await bot.get_file(info_photo.file_id)
    url = f'https://api.telegram.org/file/bot{os.getenv("USERTG")}/{file.file_path}'
    ya = YA(
            url,  
            str(info_photo.file_size) + '.jpg', 
            info_photo.file_size
            )
    ya.create_folder()
    ya.loading_profile_picture()
    dowland_url = ya.dowland_photo()
    await send_photo_vk(
                        dowland_url, 
                        msg.message_id
                        )
    
@router.message(F.document)
async def message_handler(msg: Message):
    document = msg.document
    file = await bot.get_file(document.file_id)
    url = f'https://api.telegram.org/file/bot{os.getenv("USERTG")}/{file.file_path}'
    ya = YA(
            url,  
            str(document.file_name), 
            document.file_size
            )
    ya.create_folder()
    ya.loading_profile_picture()
    dowland_url = ya.dowland_document()
    await send_document_vk(
                            dowland_url, 
                            msg.message_id, 
                            document.file_name
                            )

@router.message()
async def message_handler(msg: Message):
    await send_messages_vk(
                            msg.text, 
                            msg.message_id
                            )
    
async def on_startup(_):
    await bot.send_message(
                            os.getenv("METG"), 
                            open(
                                'info.txt', 
                                encoding="utf-8"
                                ).read()
                            )
