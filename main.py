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
    # link = await bot.get_chat_administrators(chat_id=chat_id)
    # li = await bot.export_chat_invite_link(chat_id=chat_id)
    # #print(l)
    # print(link)
#JBC3ux5knZ4j9n2
#
# class States_p(StatesGroup):
#     STATE_M = State()
#
#
# @dp.message_handler(content_types=['text'], state=None)
# async def st(message: types.Message):
#     await States_p.STATE_M.set()
#
#
# @dp.message_handler(content_types=['text'], state=States_p.STATE_M)
# async def cm_start(message: types.Message):
#     d = await bot.get_chat_members_count(chat_id)
#     print(d)
    #m = await bot.copy_message(chat_id=chat_id, from_chat_id=my_id, message_id=message.message_id)



asyncio.run(funcname())
# if __name__ == "__main__":
#     executor.start_polling(dp, skip_updates=True)