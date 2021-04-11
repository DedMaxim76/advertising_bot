import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, ContentTypeFilter
from aiogram.types import CallbackQuery, ContentType

from data import config
from filters import IsAdmin
from handlers.users.main_game.start_game import add_users_to_game, start_game
from handlers.users.top import show_top
from keyboards.inline.admin_inline_keyboards import admin_inline_menu, cancel_admin_inline_menu
from keyboards.inline.callback_datas import admin_callback, cancel_admin_callback
from loader import dp
from utils.db_api.quick_commands import user_quick_commands


@dp.message_handler(IsAdmin(), Command('admin_commands'))
async def get_admin_commands(message: types.Message):
    await message.answer(text=f"<b>За сегодня</b>: {config.ADMIN_BALANCE}\n\n"
                              f"<b>Ограничение на вывод</b>: {config.BALANCE_LIMIT}\n"
                              "Команды администратора: ",
                         reply_markup=admin_inline_menu)


@dp.callback_query_handler(cancel_admin_callback.filter(choice="pass"), state="*")
async def cancel_withdraw(call: CallbackQuery, state: FSMContext):
    await call.answer("Вы отменили дейтсвие.")
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(admin_callback.filter(command="change_limit"))
async def change_balance_limit(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer(cache_time=3)
    await call.message.answer(text="Укажите новый лимит:",
                              reply_markup=cancel_admin_inline_menu)
    await state.set_state("waiting_for_limit")


@dp.message_handler(state="waiting_for_limit")
async def change_balance_limit_finish(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Вы ввели не число, попробуйте снова.")
        await message.answer(text="Укажите новый лимит:",
                             reply_markup=cancel_admin_inline_menu)
        return
    config.BALANCE_LIMIT = int(message.text)
    await message.answer("Лимит изменен")
    await state.finish()


@dp.callback_query_handler(admin_callback.filter(command="send_everybody"))
async def take_message_everybody(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer(cache_time=3)
    await call.message.answer(text="Какое сообщение хотите отправить?",
                              reply_markup=cancel_admin_inline_menu)
    await state.set_state("waiting_for_message_to_send_everybody")


@dp.message_handler(content_types=ContentType.PHOTO, state="waiting_for_message_to_send_everybody")
@dp.message_handler(content_types=ContentType.DOCUMENT, state="waiting_for_message_to_send_everybody")
@dp.message_handler(content_types=ContentType.TEXT, state="waiting_for_message_to_send_everybody")
async def send_message_everybody(message: types.Message, state: FSMContext):
    users = await user_quick_commands.select_all_users()
    for user in users:
        await message.send_copy(chat_id=user.id)
    await message.answer("Рассылка выполнена!")
    await state.finish()


@dp.callback_query_handler(admin_callback.filter(command="start_game"))
async def start_RM_game(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer(cache_time=3)
    await add_users_to_game()
    await asyncio.sleep(10)
    await start_game()


@dp.callback_query_handler(admin_callback.filter(command="show_top"))
async def send_top(call: CallbackQuery):
    await show_top()

