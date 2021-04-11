from aiogram.types import CallbackQuery

from keyboards.inline.account_inline_menu import back_menu
from keyboards.inline.callback_datas import info_callback
from loader import dp


@dp.callback_query_handler(info_callback.filter(choice="chat"))
async def chat_info_show(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(text=""" 1""",
                              reply_markup=back_menu)