from multiprocessing import Process
from YA import *
from Fishing_VK import VK
from Fishing_TG import TG
import asyncio


class main:

    def __init__(self):
        self.vk = VK
        self.tg = TG

    def start_vk(self):
        vk = VK
        vk.fishing_start()

    def start_tg(self):
        tg = TG
        tg.fishing_start()

# Запуск программы

# class transit(main):
    
#     def accept_forward_text(self, text, identifier, random_id):
#         if identifier == 'vk':
#             asyncio.run(self.vk.accept_message(text, random_id))
#         if identifier == 'tg':
#             self.tg.accept_message(text)

if __name__ == '__main__':
    start = main
    g1 = Process(target=start.start_vk)
    g2 = Process(target=start.start_tg)
    g1.start()
    g2.start()
    g1.join()
    g2.join()