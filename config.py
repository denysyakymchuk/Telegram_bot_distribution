from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

logging.basicConfig(level=logging.INFO)

API_TOKEN = '5258758589:AAGACEmLckq-rjnHBAfw_j7h8JuDzm_anaU'  # Ваш токен API для бота
API_ID = '27322225'  # Ваш API ID из приложения Telegram
API_HASH = '51450dc7b2e95da2f1e951a3a225df1e'  # Ваш API Hash из приложения Telegram

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)