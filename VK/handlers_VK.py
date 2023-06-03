from vkbottle import User
from vkbottle.user import Message
import os
from Bot.send import send_messages_tg

bot = User(os.getenv("USERVK"))
peer_id = os.getenv("KATEVK")

@bot.on.private_message()
async def catching_message(ms: Message):
    if ms.peer_id == peer_id:
        await send_messages_tg(ms.text)


    

