from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink

from data import config
from keyboards.inline.account_inline_menu import back_menu
from keyboards.inline.callback_datas import info_callback
from loader import dp


@dp.callback_query_handler(info_callback.filter(choice="game"))
async def game_info_show(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer_photo(photo="https://ibb.co/TLnbrGM",
                                    caption=f"""🎲 Мини игра RM
└ RANDOM MONEY- мини-игра от {hlink("Vital Change", config.MAIN_CHANNEL_URL)}!
Наш социальный проект представляет мини-игру, которая позволит пользователям нашего продукта испытать свою удачу и посмотреть, повернется ли фортуна лицом к Вам!

С Вашего счета один раз в день будет списываться 1 монета.
Куда она перейдет?
Случайному пользователю, со счета которого тоже спишется 1 монета.
Испытай свою удачу, получи рандомное количество монет в обмен на 1 свою!""",
                                    reply_markup=back_menu)


@dp.callback_query_handler(info_callback.filter(choice="WTF_game"))
async def game_WTF_info_show(call: CallbackQuery):
    await call.message.delete_reply_markup()
    await call.message.answer_photo(photo="https://ibb.co/TLnbrGM",
                                    caption=f"""🎲 Мини игра RM
    └ RANDOM MONEY- мини-игра от {hlink("Vital Change", config.MAIN_CHANNEL_URL)}!
    Наш социальный проект представляет мини-игру, которая позволит пользователям нашего продукта испытать свою удачу и посмотреть, повернется ли фортуна лицом к Вам!

    С Вашего счета один раз в день будет списываться 1 монета.
    Куда она перейдет?
    Случайному пользователю, со счета которого тоже спишется 1 монета.
    Испытай свою удачу, получи рандомное количество монет в обмен на 1 свою!""")
