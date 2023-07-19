import openai
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData


openai.api_key = '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'

logging.basicConfig(level=logging.INFO)

API_TOKEN = '5873031277:AAEIQ9RChp2mEHlSqbAspGHFH7Qtauj2Sb8'  # Ваш токен API для бота


engine = create_engine("mysql+mysqlconnector://root:1234567890@127.0.0.1:3306/test", echo=True)
conn = engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

metadata_obj = MetaData()

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
