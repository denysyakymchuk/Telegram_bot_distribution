from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData


logging.basicConfig(level=logging.INFO)

API_TOKEN = '5213744918:AAGJ0soqQPOyn1wgY2_5FYgMOw8lQrbdyKQ'  # Ваш токен API для бота
API_ID = ''  # Ваш API ID из приложения Telegram
API_HASH = ''  # Ваш API Hash из приложения Telegram


engine = create_engine("mysql+mysqlconnector://root:1234567890@127.0.0.1:3306/test", echo=True)
conn = engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

metadata_obj = MetaData()

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
