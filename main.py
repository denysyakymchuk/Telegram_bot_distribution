import sqlalchemy
from aiogram import types
from aiogram.bot import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from sqlalchemy.orm import state
from telethon.sync import TelegramClient
from telethon import functions
from config import dp, API_ID, API_HASH, session, conn, engine
from keyboard import buttons_start, key_group, key_user
from models import group, user


# States
class Form(StatesGroup):
    message = State()


class FormGroup(StatesGroup):
    link = State()

class FormUser(StatesGroup):
    api_id = State()
    api_hash = State()
    phone_number = State()

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply("Привіт!", reply_markup=buttons_start)
#-------------------------------------------------------------#

@dp.message_handler(commands='user')
async def user_func(message: types.Message):
    await message.reply("Вибери  дію: ", reply_markup=key_user)


@dp.message_handler(commands='see')
async def see_user(message: types.Message):
    users = sqlalchemy.select(user)
    select_r = conn.execute(users)
    await message.reply(select_r.fetchall(), reply_markup=buttons_start)

@dp.message_handler(commands='create')
async def create_user(message: types.Message):
    await message.reply("Введи api_id: ", reply_markup=key_group)
    await FormUser.api_id.set()


@dp.message_handler(state=FormUser.api_id)
async def fsm_api_id_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['api_id'] = message.text
    await message.reply("Введи api_hash: ", reply_markup=key_group)
    await FormUser.api_hash.set()


@dp.message_handler(state=FormUser.api_hash)
async def fsm_api_id_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['api_hash'] = message.text
    await message.reply("Введи номер телефону: ", reply_markup=key_group)
    await FormUser.phone_number.set()


@dp.message_handler(state=FormUser.phone_number)
async def fsm_api_id_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await message.reply("Дані записано: ", reply_markup=buttons_start)
    with engine.connect() as conn:
        dt = user.insert().values(api_id=data['api_id'], api_hash=data['api_hash'], phone_number=data['phone_number'])
        conn.execute(dt)
        conn.commit()
    await state.finish()


#-------------------------------------------------------------#

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
#-------------------------------------------------------------#


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