import asyncio
import logging
from multiprocessing import Process
from VK.run_VK import run_vk
from TG.run_TG import run_tg

def start_tg():
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_tg())

def start_vk():
    run_vk()

if __name__ == "__main__":
    Vkontacte = Process(target=start_vk)
    Telegram = Process(target=start_tg)
    Vkontacte.start()
    Telegram.start()
    Vkontacte.join()
    Telegram.join()