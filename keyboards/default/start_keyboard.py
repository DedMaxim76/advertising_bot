from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👤 Личный кабинет"),
        ],
    ],
    resize_keyboard=True)

start_menu_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👤 Личный кабинет"),
        ],
        [
            KeyboardButton(text="👨🏻‍💻 Админ панель"),
        ],
    ],
    resize_keyboard=True)