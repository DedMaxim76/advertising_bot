from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import payment_method_callback, accept_phone_callback, accept_card_callback, \
    cancel_callback

withdraw_inline_menu = InlineKeyboardMarkup(row_width=2,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(text="🥝 Qiwi",
                                                                         callback_data=payment_method_callback.new(
                                                                             method="qiwi")),
                                                    InlineKeyboardButton(text="💳 Карта",
                                                                         callback_data=payment_method_callback.new(
                                                                             method="card")),
                                                ],
                                            ])

accept_phone_inline_menu = InlineKeyboardMarkup(row_width=2,
                                                inline_keyboard=[
                                                    [
                                                        InlineKeyboardButton(text="Да",
                                                                             callback_data=accept_phone_callback.new(
                                                                                 choice="yes")),
                                                        InlineKeyboardButton(text="Нет",
                                                                             callback_data=accept_phone_callback.new(
                                                                                 choice="no")),
                                                    ],
                                                ])
accept_card_inline_menu = InlineKeyboardMarkup(row_width=2,
                                               inline_keyboard=[
                                                   [
                                                       InlineKeyboardButton(text="Да",
                                                                            callback_data=accept_card_callback.new(
                                                                                choice="yes")),
                                                       InlineKeyboardButton(text="Нет",
                                                                            callback_data=accept_card_callback.new(
                                                                                choice="no")),
                                                   ],
                                               ])
cancel_inline_menu = InlineKeyboardMarkup(row_width=1,
                                          inline_keyboard=[
                                              [
                                                  InlineKeyboardButton(text="Отмена",
                                                                       callback_data=cancel_callback.new(
                                                                           withdraw_method="pass")),
                                              ],
                                          ],
                                          )
