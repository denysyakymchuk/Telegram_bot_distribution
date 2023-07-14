import sqlalchemy
from aiogram import types
from aiogram.bot import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from telethon.sync import TelegramClient
from telethon import functions
from config import dp, API_ID, API_HASH, session, conn, engine
from keyboard import buttons_start, key_group, key_user
from models import group


# States
class Form(StatesGroup):
    message = State()


class FormGroup(StatesGroup):
    link = State()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply("Привіт!", reply_markup=buttons_start)


@dp.message_handler(commands='user')
async def user_func(message: types.Message):
    await message.reply("Вибери  дію: ", reply_markup=key_user)


@dp.message_handler(commands='group')
async def group_func(message: types.Message):
    await message.reply("Вибери  дію: ", reply_markup=key_group)


@dp.message_handler(commands='new')
async def new_group(message: types.Message):
    await message.reply('Введи лінк до групи:', reply_markup=key_group)
    await FormGroup.link.set()


@dp.message_handler(state=FormGroup.link)
async def process_link(message: types.Message, state: FSMContext):
    with engine.connect() as conn:
        link_fresh = group.insert().values(link=message.text)
        conn.execute(link_fresh)
        conn.commit()
    await message.reply('Дані успішно записані!', reply_markup=buttons_start)
    await state.finish()


@dp.message_handler(commands='list')
async def group_func(message: types.Message):
    select = sqlalchemy.select(group)
    select_r = conn.execute(select)
    await message.reply(select_r.fetchall(), reply_markup=buttons_start)


@dp.message_handler(commands='sms')
async def build_sms(message: types.Message):
    await Form.message.set()
    await message.reply("Введіть повідомлення для відправки:")


@dp.message_handler(state=Form.message)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message'] = message.text

    await state.finish()

    async with TelegramClient('session_name', API_ID, API_HASH) as client:
        await client.start()
        names = ['https://t.me/Denchyk_p']
        for name in names:
            result = await client(functions.messages.SendMessageRequest(
                peer=name,
                message=data['message']
            ))
        await client.disconnect()

    await message.reply("Повідомлення успішно записано!")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)