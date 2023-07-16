import sqlalchemy
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from telethon.sync import TelegramClient
from telethon import functions
from config import dp, session, conn, engine, bot
from keyboard import buttons_start, key_group, key_user
from models import group, user


# States for send sms
class Form(StatesGroup):
    select_user = State()
    insert_veryf_code = State()
    message = State()


# States for insert group
class FormGroup(StatesGroup):
    link = State()


# States for insert user data
class FormUser(StatesGroup):
    api_id = State()
    api_hash = State()
    phone_number = State()


# main start command. Return message and main keyboard
@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply("Привіт!", reply_markup=buttons_start)


# --------------------------USER BLOCK-----------------------------------#

@dp.message_handler(commands='user')
async def user_func(message: types.Message):
    await message.reply("Вибери  дію: ", reply_markup=key_user)


# return list of users
@dp.message_handler(commands='see')
async def see_user(message: types.Message):
    users = sqlalchemy.select(user)
    select_r = conn.execute(users)
    await message.reply(select_r.fetchall(), reply_markup=buttons_start)


# start states for create user
@dp.message_handler(commands='create')
async def create_user(message: types.Message):
    await message.reply("Введи api_id: ", reply_markup=key_group)
    await FormUser.api_id.set()


# state for insert api_id user
@dp.message_handler(state=FormUser.api_id)
async def fsm_api_id_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['api_id'] = message.text
    await message.reply("Введи api_hash: ", reply_markup=key_group)
    await FormUser.api_hash.set()


# state for insert api_hash user
@dp.message_handler(state=FormUser.api_hash)
async def fsm_api_id_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['api_hash'] = message.text
    await message.reply("Введи номер телефону: ", reply_markup=key_group)
    await FormUser.phone_number.set()


# state for insert phone_number user
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


# -------------------------------GROUP BLOCK------------------------------#

# return keyboard: list of group and new group link
@dp.message_handler(commands='group')
async def group_func(message: types.Message):
    await message.reply("Вибери  дію: ", reply_markup=key_group)


# insern new group
@dp.message_handler(commands='new')
async def new_group(message: types.Message):
    await message.reply('Введи лінк до групи:', reply_markup=key_group)
    await FormGroup.link.set()


# states insert link group
@dp.message_handler(state=FormGroup.link)
async def process_link(message: types.Message, state: FSMContext):
    with engine.connect() as conn:
        link_fresh = group.insert().values(link=message.text)
        conn.execute(link_fresh)
        conn.commit()
    await message.reply('Дані успішно записані!', reply_markup=buttons_start)
    await state.finish()


# return list og groups
@dp.message_handler(commands='list')
async def group_func(message: types.Message):
    select = sqlalchemy.select(group)
    select_r = conn.execute(select)
    await message.reply(select_r.fetchall(), reply_markup=buttons_start)


# ------------------------------SMS BLOCK-------------------------------#

# start states for sms and return all users for select in NEXT state
@dp.message_handler(commands='sms')
async def build_sms(message: types.Message):
    await message.reply("Виберіть номер користувача для відправки:")
    with engine.connect() as conn:
        usr = sqlalchemy.select(user)
        users = conn.execute(usr).fetchall()

    await message.reply(f"{users}")
    await Form.select_user.set()


# select user
@dp.message_handler(state=Form.select_user)
async def fsm_select_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['select_user'] = message.text

    # await message.reply('Введи повідомлення:')
    global clientt, usr
    usr = session.query(user).filter_by(id=data['select_user']).first()

    clientt = TelegramClient('session_name', int(usr[1]), str(usr[2]))

    try:
        await clientt.start(phone=usr[3])
        await clientt.send_code_request(str(usr[3]))
    except:
        None

    await message.reply('Введи верифікаційний код:')
    await Form.insert_veryf_code.set()


# authorization of user
@dp.message_handler(state=Form.insert_veryf_code)
async def insert_ver_code(message: types.Message, state: FSMContext):
    await clientt.sign_in(code=message.text)
    await message.reply('Введи повідомлення:')
    await Form.message.set()


# write message
@dp.message_handler(state=Form.message)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message'] = message.text

    await state.finish()

    # select data from db

    # Отправка запроса на генерацию кода подтверждения Telethon
    # await client.send_code_request(str(usr[3]))

    # create client and send sms
    async with TelegramClient('session_name', int(usr[1]), str(usr[2])) as client:
        await client.start()
        names = ['https://t.me/Denchyk_p']

        for name in names:
            result = await client(functions.messages.SendMessageRequest(
                peer=name,
                message=data['message']
            ))
        await client.disconnect()

    await message.reply("Повідомлення успішно відправлено!")


# точка входа
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
