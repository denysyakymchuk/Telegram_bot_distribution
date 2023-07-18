from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

sms = KeyboardButton('/sms')
group = KeyboardButton('/group')
message = KeyboardButton('/user')
buttons_start = ReplyKeyboardMarkup(resize_keyboard=True).add(sms, group, message)

new_group = KeyboardButton('/new')
list_group = KeyboardButton('/list')
delete_group = KeyboardButton('/delete🚫')
key_group = ReplyKeyboardMarkup(resize_keyboard=True).add(new_group, list_group, delete_group)

all_groups = KeyboardButton('/all')
select_groups = KeyboardButton('/select')
send_key_groups = ReplyKeyboardMarkup(resize_keyboard=True).add(all_groups, select_groups)

new_user = KeyboardButton('/create')
list_user = KeyboardButton('/see')
delete_user = KeyboardButton('/delete⛔')
key_user = ReplyKeyboardMarkup(resize_keyboard=True).add(new_user, list_user, delete_user)