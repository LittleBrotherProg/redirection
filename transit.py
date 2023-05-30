from Fishing_TG import TG
from Fishing_VK import VK
import asyncio

class fish:

    def __init__(self):
        self.vk = VK
        self.tg = TG

    def accept_forward_text(self, text, identifier, random_id):
        if identifier == 'vk':
            asyncio.run(self.vk.accept_message(text, random_id))
        if identifier == 'tg':
            self.tg.accept_message(text)
