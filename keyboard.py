from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

sms = KeyboardButton('/sms')
group = KeyboardButton('/group')
message = KeyboardButton('/user')
buttons_start = ReplyKeyboardMarkup(resize_keyboard=True).add(sms, group, message)

new_group = KeyboardButton('/new')
list_group = KeyboardButton('/list')
key_group = ReplyKeyboardMarkup(resize_keyboard=True).add(new_group, list_group)


new_user = KeyboardButton('/New')
list_user = KeyboardButton('/List')
key_user = ReplyKeyboardMarkup(resize_keyboard=True).add(new_user, list_user)