from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import admin_callback, cancel_admin_callback

admin_inline_menu = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✉️ Сделать рассылку",
                                 callback_data=admin_callback.new(
                                     command="send_everybody"))
        ],
        [
            InlineKeyboardButton(text="📊 Изменить лимит",
                                 callback_data=admin_callback.new(
                                     command="change_limit")),
        ],
        [
            InlineKeyboardButton(text="Игра RM",
                                 callback_data=admin_callback.new(
                                     command="start_game")),
        ],
        [
            InlineKeyboardButton(text="Топ пользователей",
                                 callback_data=admin_callback.new(
                                     command="show_top")),
        ],
    ])

cancel_admin_inline_menu = InlineKeyboardMarkup(row_width=1,
                                                inline_keyboard=[
                                                    [
                                                        InlineKeyboardButton(text="Отмена",
                                                                             callback_data=cancel_admin_callback.new(
                                                                                 choice="pass")),
                                                    ],
                                                ],
                                                )
