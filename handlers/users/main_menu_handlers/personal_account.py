from aiogram import types
from aiogram.types import CallbackQuery

from handlers.users.top import show_top
from keyboards.inline.account_inline_menu import account_menu, info_menu
from keyboards.inline.callback_datas import info_callback, back_callback
from loader import dp
from utils.db_api.quick_commands import user_quick_commands
from utils.db_api.schemas.users import User


@dp.message_handler(text="👤 Личный кабинет")
async def send_menu_personal_account(message: types.Message):
    user: User = await user_quick_commands.select_user(message.from_user.id)
    deep_link = "https://t.me/test_chatex_bot?start=" + user.referral_code
    print(deep_link)
    await message.answer_photo(photo="https://ibb.co/TLnbrGM",
                               caption=f"<b>Ваш баланс</b>: {user.balance} монет\n\n"
                                       f"👥 <b>Реферальная система</b>\n"
                                       f"├ <b>Активных</b>: {user.num_of_active_referrals} участников\n"
                                       f"└ <b>Ожидание</b>: {user.num_of_passive_referrals} участников\n\n"
                                       f"🗣 <b>Пригласительная ссылка</b>\n"
                                       f"└ {deep_link}",
                               reply_markup=account_menu)


@dp.callback_query_handler(info_callback.filter(choice="main"))
async def send_info_to_user(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("""Что вам интересно?
""",
                              reply_markup=info_menu)


@dp.callback_query_handler(back_callback.filter(from_where="any"))
async def back_to_main_info(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("""Что вам интересно?
    """,
                              reply_markup=info_menu)



