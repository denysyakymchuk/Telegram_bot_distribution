import os

import sqlalchemy
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from sqlalchemy import delete
from telethon.sync import TelegramClient
from telethon import functions

import tools
from config import dp, session, conn, engine, bot
from keyboard import buttons_start, key_group, key_user, send_key_groups
from models import group, user
from tools import ref_data
from log import write_logs


# States for send sms
class Form(StatesGroup):
    select_group = State()
    optional_groups = State()
    select_user = State()
    insert_veryf_code = State()
    message = State()


# States for insert group
class FormGroup(StatesGroup):
    link = State()


class FormGroupDelete(StatesGroup):
    id_group = State()


# States for insert user data
class FormUser(StatesGroup):
    title = State()
    api_id = State()
    api_hash = State()
    phone_number = State()


class FormUserDelete(StatesGroup):
    id_user = State()


# main start command. Return message and main keyboard
@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply("Привіт!", reply_markup=buttons_start)


# --------------------------USER BLOCK-----------------------------------#

@dp.message_handler(commands='user')
async def user_func(message: types.Message):
    await message.reply("Вибери дію: ", reply_markup=key_user)


# return list of users
@dp.message_handler(commands='see')
async def see_user(message: types.Message):
    try:
        users = sqlalchemy.select(user.c.id, user.c.title)
        select_r = conn.execute(users)

        await message.reply(ref_data(select_r.fetchall()), reply_markup=buttons_start)

    except Exception as error:
        write_logs(error)
        await message.reply('Помилка! Спробуйте ще раз за декілька хвилин!')


# start states for create user
@dp.message_handler(commands='create')
async def create_user(message: types.Message):
    try:
        await message.reply("Введи назву користувача: ", reply_markup=key_group)
        await FormUser.title.set()

    except Exception as error:
        write_logs(error)
        await message.reply('Помилка! Спробуйте ще раз за декілька хвилин!')


@dp.message_handler(state=FormUser.title)
async def fsm_api_id_user(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['title'] = message.text
        await message.reply("Введи api_id: ", reply_markup=key_group)
        await FormUser.api_id.set()

    except Exception as error:
        write_logs(error)
        await message.reply('Помилка! Спробуйте ще раз!\nПеревірте введені дані')
        await state.finish()


# state for insert api_id user
@dp.message_handler(state=FormUser.api_id)
async def fsm_api_id_user(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['api_id'] = message.text
        await message.reply("Введи api_hash: ", reply_markup=key_group)
        await FormUser.api_hash.set()

    except Exception as error:
        write_logs(error)
        await message.reply('Помилка! Спробуйте ще раз!\nПеревірте введені дані')
        await state.finish()


# state for insert api_hash user
@dp.message_handler(state=FormUser.api_hash)
async def fsm_api_id_user(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['api_hash'] = message.text
        await message.reply("Введи номер телефону: ", reply_markup=key_group)
        await FormUser.phone_number.set()

    except Exception as error:
        write_logs(error)
        await message.reply('Помилка! Спробуйте ще раз!\nПеревірте введені дані')
        await state.finish()


# state for insert phone_number user
@dp.message_handler(state=FormUser.phone_number)
async def fsm_api_id_user(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['phone_number'] = message.text

        with engine.connect() as conn:
            dt = user.insert().values(title=data['title'], api_id=data['api_id'], api_hash=data['api_hash'], phone_number=data['phone_number'])
            conn.execute(dt)
            conn.commit()

        await state.finish()
        await message.reply("Дані записано: ", reply_markup=buttons_start)

    except Exception as error:
        write_logs(error)
        await message.reply('Помилка! Спробуйте ще раз!\nПеревірте введені дані')
        await state.finish()


@dp.message_handler(commands='delete⛔')
async def delete_group(message: types.Message):
    try:
        await message.reply('Введи номер групи для видалення:', reply_markup=buttons_start)
        select = sqlalchemy.select(user)
        select_r = conn.execute(select)

        await message.reply(f'{ref_data(select_r.fetchall())}')
        await FormUserDelete.id_user.set()

    except Exception as error:
        write_logs(error)
        await message.reply('Помилка! Спробуйте ще раз!\nПеревірте введені дані')


@dp.message_handler(state=FormUserDelete.id_user)
async def deleting_group(message: types.Message, state: FSMContext):
    try:
        delete_statement = delete(user).where(user.c.id == message.text)
        # Выполнение операции удаления
        conn.execute(delete_statement)
        conn.commit()
        await message.reply('Користувача видалено!', reply_markup=buttons_start)
        await state.finish()

    except Exception as error:
        write_logs(error)
        await message.reply('Помилка! Спробуйте ще раз!\nПеревірте введені дані')
        await state.finish()

# -------------------------------GROUP BLOCK------------------------------#


# return keyboard: list of group and new group link
@dp.message_handler(commands='group')
async def group_func(message: types.Message):
    await message.reply("Вибери дію: ", reply_markup=key_group)


# insert new group
@dp.message_handler(commands='new')
async def new_group(message: types.Message):
    try:
        await message.reply('Введи лінк до групи:', reply_markup=key_group)
        await FormGroup.link.set()

    except Exception as error:
        write_logs(error)
        await message.reply('Помилка! Спробуйте ще раз за деілька хвилин!')


# states insert link group
@dp.message_handler(state=FormGroup.link)
async def process_link(message: types.Message, state: FSMContext):
    try:
        with engine.connect() as conn:
            link_fresh = group.insert().values(link=message.text)
            conn.execute(link_fresh)
            conn.commit()
        await message.reply('Дані успішно записані!', reply_markup=buttons_start)
        await state.finish()

    except Exception as error:
        write_logs(error)
        await message.reply('Помилка! Спробуйте ще раз!\nПеревірте введені дані')
        await state.finish()


# return list og groups
@dp.message_handler(commands='list')
async def group_func(message: types.Message):
    try:
        select = sqlalchemy.select(group)
        select_r = conn.execute(select)
        await message.reply(ref_data(select_r.fetchall()), reply_markup=buttons_start)

    except Exception as error:
        write_logs(error)
        await message.reply('Помилка! Спробуйте ще раз за деілька хвилин!')


# delete group
@dp.message_handler(commands='delete🚫')
async def delete_group(message: types.Message):
    try:
        await message.reply('Введи номер групи для видалення:', reply_markup=buttons_start)
        select = sqlalchemy.select(group)
        select_r = conn.execute(select)

        await message.reply(f'{ref_data(select_r.fetchall())}')
        await FormGroupDelete.id_group.set()

    except Exception as error:
        write_logs(error)
        await message.reply('Помилка! Спробуйте ще раз за декілька хвилин!')


@dp.message_handler(state=FormGroupDelete.id_group)
async def deleting_group(message: types.Message, state: FSMContext):
    try:
        delete_statement = delete(group).where(group.c.id == message.text)
        # Выполнение операции удаления
        conn.execute(delete_statement)
        conn.commit()
        await message.reply('Групу видалено!', reply_markup=buttons_start)
        await state.finish()

    except Exception as error:
        write_logs(error)
        await message.reply('Помилка! Спробуйте ще раз!\nПеревірте введені дані')
        await state.finish()

# ------------------------------SMS BLOCK-------------------------------#


# start states for sms and return all users for select in NEXT state
@dp.message_handler(commands='sms')
async def build_sms(message: types.Message):
    if os.path.exists('session.session'):
        # Delete file
            os.remove('session.session')
    try:
        await message.reply("Виберіть номер користувача для відправки:")

        with engine.connect() as conn:
            usr = sqlalchemy.select(user)
            users = conn.execute(usr).fetchall()

        await message.reply(f"{ref_data(users)}")
        await Form.select_user.set()

    except Exception as error:
        write_logs(error)
        await message.reply('Помилка! Спробуйте ще раз!\nПеревірте введені дані')


# select user
@dp.message_handler(state=Form.select_user)
async def fsm_select_user(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['select_user'] = message.text

        global clientt, usr
        usr = session.query(user).filter_by(id=data['select_user']).first()

        async with state.proxy() as data:
            data['alias'] = usr[1]

        clientt = TelegramClient('session', api_id=int(usr[2]), api_hash=str(usr[3]))

        await clientt.start(phone=usr[4])
        await clientt.send_code_request(str(usr[4]))

        await message.reply('Введи верифікаційний код:')
        await Form.insert_veryf_code.set()

    except Exception as error:
        write_logs(error)
        await message.reply('Введи верифікаційний код:')
        await Form.insert_veryf_code.set()


# authorization of user
@dp.message_handler(state=Form.insert_veryf_code)
async def insert_ver_code(message: types.Message, state: FSMContext):
    try:
        await clientt.sign_in(code=message.text)
        await message.reply('Вибери групи:', reply_markup=send_key_groups)
        await Form.select_group.set()

    except Exception as error:
        write_logs(error)
        await message.reply('Помилка! Спробуйте ще раз!\nПеревірте введені дані')
        await state.finish()


@dp.message_handler(state=Form.select_group)
async def process_select_group(message: types.Message, state: FSMContext):
    if message.text == '/all':
        async with state.proxy() as data:
            data['groups'] = True
        await message.reply('Введи повідомлення:', reply_markup=key_group)
        await Form.message.set()

    elif message.text == '/select':
        async with state.proxy() as data:
            data['groups'] = False
        await message.reply('Введи номера груп в котрі потрібно надіслати повідомлення:\nПриклад: 1, 3, 5', reply_markup=key_group)

        with engine.connect() as conn:
            gr = sqlalchemy.select(group)
            g = conn.execute(gr).fetchall()

        await message.reply(f"{ref_data(g)}")

        await Form.optional_groups.set()


@dp.message_handler(state=Form.optional_groups)
async def optional_selecting_groups(message: types.Message, state: FSMContext):
    id_list = [int(x) for x in message.text.split(',')]
    async with state.proxy() as data:
        data['selected_groups'] = id_list

    await message.reply('Введи повідомлення:')
    await Form.message.set()


# write message
@dp.message_handler(state=Form.message)
async def process_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['message'] = message.text

        await state.finish()

        global value_list
        value_list = []

        if data['groups'] is True:
            stmt = sqlalchemy.select(group.c.link)
            result = conn.execute(stmt)
            column_values = result.fetchall()

            value_list = [value for (value,) in column_values]

        else:
            stmt = sqlalchemy.select(group.c.link).where(group.c.id.in_(data['selected_groups']))
            column_values = session.execute(stmt).fetchall()
            value_list = [value for (value,) in column_values]
        error_send = []

        q = f'''
         chatgpt пожалуйста поздоровайся со всеми учасниками группы от имени {data['alias']}, группа не {data['alias']} -
         мы просто здороваемся от этого имени, не спрашивай как дела просто поздоровайся, можешь пожелать всем продуктивного 
         дня и добавь пару смайликов'''

        for name in value_list:
            # try:
            result = await clientt(functions.messages.SendMessageRequest(
                peer=name,
                message=tools.generate_response(q)
            ))
            # except:
            #     error_send.append(name)

        await clientt.disconnect()

        await message.reply(f"Повідомлення успішно відправлено!\nПропущені: {error_send}")

    except Exception as error:
        write_logs(error)
        await message.reply('Помилка! Спробуйте ще раз!\nПеревірте введені дані')
        await state.finish()

# place enter
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
