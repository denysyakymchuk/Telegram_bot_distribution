from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

sms = KeyboardButton('/sms')
group = KeyboardButton('/group')
message = KeyboardButton('/message')
buttons_start = ReplyKeyboardMarkup(resize_keyboard=True).add(sms, group, message)