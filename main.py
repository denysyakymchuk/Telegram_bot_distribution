from datetime import datetime, timedelta
import asyncio
from aiogram import *
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiohttp
session = aiohttp.ClientSession()
#use the session here



TOKEN = '5213744918:AAGJ0soqQPOyn1wgY2_5FYgMOw8lQrbdyKQ'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
chat_id = -746607958


async def funcname():
    l = await bot.get_chat(chat_id)
    print(l)

#JBC3ux5knZ4j9n2



asyncio.run(funcname())
