if __name__ != "__main__":
  import os
  from dotenv import load_dotenv, find_dotenv
  from aiogram import Bot, Dispatcher
  from aiogram.contrib.fsm_storage.memory import MemoryStorage

  load_dotenv(find_dotenv())
  storage = MemoryStorage()
  bot = Bot(token=os.getenv('TOKEN'), parse_mode='HTML')
  dp = Dispatcher(bot, storage=storage)
