from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from telethon.sync import TelegramClient
from telethon import functions

from config import dp, API_ID, API_HASH


# States
class Form(StatesGroup):
    message = State()

@dp.message_handler(commands='sms')
async def cmd_start(message: types.Message):
    await Form.message.set()
    await message.reply("Введите сообщение для отправки:")

@dp.message_handler(state=Form.message)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message'] = message.text

    await state.finish()

    async with TelegramClient('session_name', API_ID, API_HASH) as client:
        await client.start()
        names = ['https://t.me/nix_cash', 'https://t.me/ValerkaHell']
        for name in names:
            result = await client(functions.messages.SendMessageRequest(
                peer=name,
                message=data['message']
            ))
        await client.disconnect()

    await message.reply("Сообщение успешно отправлено!")

    # Отправка SMS-сообщения
    with TelegramClient('session_name', API_ID, API_HASH) as client:
        client.send_message('your_phone_number', data['message'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)