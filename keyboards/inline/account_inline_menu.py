from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import config
from keyboards.inline.callback_datas import withdraw_callback, info_callback, balance_callback, back_callback

account_menu = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text="💸 Вывод",
                                                                 callback_data=balance_callback.new(event="withdraw")),
                                            InlineKeyboardButton(text="🔮 Инфо",
                                                                 callback_data=info_callback.new(choice="main")),
                                        ],
                                    ])

info_menu = InlineKeyboardMarkup(row_width=1,
                                 inline_keyboard=[
                                     [
                                         InlineKeyboardButton(text="Реферальная система",
                                                              callback_data=info_callback.new(choice="referral")),
                                     ],
                                     [
                                         InlineKeyboardButton(text="Чат пользователей",
                                                              url=config.MAIN_CHAT_URL),
                                     ],
                                     [
                                         InlineKeyboardButton(text="Мини игра RM",
                                                              callback_data=info_callback.new(choice="game")),
                                     ],
                                 ])
game_info_menu = InlineKeyboardMarkup(row_width=1,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text="Что за мини игра RM?",
                                                                   callback_data=info_callback.new(choice="WTF_game")),
                                          ],
                                      ])

chat_menu = InlineKeyboardMarkup(row_width=1,
                                 inline_keyboard=[
                                     [
                                         InlineKeyboardButton(text="Чат пользователей",
                                                              url="https://t.me/joinchat/-EJrbbj8pm9hNTYy"),
                                     ],
                                 ])

back_menu = InlineKeyboardMarkup(row_width=1,
                                 inline_keyboard=[
                                     {
                                         InlineKeyboardButton(text="Назад",
                                                              callback_data=back_callback.new(from_where="any"))
                                     }
                                 ])
