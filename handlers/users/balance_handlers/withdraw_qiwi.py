from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink

from data import config
from keyboards.inline.callback_datas import balance_callback, payment_method_callback, accept_phone_callback
from keyboards.inline.withdraw_inline_menu import withdraw_inline_menu, accept_phone_inline_menu, cancel_inline_menu
from loader import dp, bot
from utils.db_api.quick_commands import user_quick_commands
from utils.db_api.schemas.users import User
from utils.misc.qiwi import Payment

Max_Withdraw = 1000
Min_Withdraw = 10
Card_Fee = 50


@dp.callback_query_handler(balance_callback.filter(event="withdraw"))
async def withdraw(call: CallbackQuery):
    await call.answer(cache_time=2)
    await call.message.edit_reply_markup()
    await call.message.answer(text="<b>Какой способ вывода хотите выбрать?</b>\n\n"
                                   "Комиссия на qiwi - 2%\n"
                                   "Комиссия на карту - 2% + 50 руб.",
                              reply_markup=withdraw_inline_menu)


@dp.callback_query_handler(payment_method_callback.filter(method="qiwi"))
async def withdraw_qiwi(call: CallbackQuery, state: FSMContext):
    user: User = await user_quick_commands.select_user(call.from_user.id)
    await call.message.delete()
    if user.phone:
        await call.message.answer(text=f"Вывести средства по этому номеру телефона {user.phone}?",
                                  reply_markup=accept_phone_inline_menu)
        await state.set_state("waiting_for_accept_phone")
        return
    await call.message.answer(text="<b>Введите номер телефона вашего кошелька:</b>",
                              reply_markup=cancel_inline_menu)
    await state.set_state("waiting_for_phone_qiwi")


@dp.callback_query_handler(accept_phone_callback.filter(choice="yes"), state="waiting_for_accept_phone")
async def withdraw_phone_accept(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Сколько хотите вывести?",
                              reply_markup=cancel_inline_menu)
    await state.set_state("waiting_for_amount_to_withdraw")


@dp.callback_query_handler(accept_phone_callback.filter(choice="no"), state="waiting_for_accept_phone")
async def withdraw_phone_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await user_quick_commands.change_phone(call.from_user.id)
    await call.message.answer(text="Введите номер телефона вашего кошелька:",
                              reply_markup=cancel_inline_menu)
    await state.set_state("waiting_for_phone_qiwi")


@dp.message_handler(state="waiting_for_phone_qiwi")
async def withdraw_phone(message: types.Message, state: FSMContext):
    phone = message.text
    await user_quick_commands.change_phone(message.from_user.id, phone)
    await message.answer("Номер телефона будет закреплен за Вами.")
    await message.answer("Сколько хотите вывести?",
                         reply_markup=cancel_inline_menu)
    await state.set_state("waiting_for_amount_to_withdraw")


@dp.message_handler(state="waiting_for_amount_to_withdraw")
async def withdraw_qiwi_send(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Вы ввели не число, попробуйте снова.")
        await message.answer("Сколько хотите вывести?",
                             reply_markup=cancel_inline_menu)
        return
    user: User = await user_quick_commands.select_user(message.from_user.id)
    amount = float(message.text)
    amount_with_fee = amount * 0.98
    if amount > Max_Withdraw or amount < Min_Withdraw:
        await message.answer("Минимальная сума вывода 10 рублей.\n"
                             "Максимальная 1000 рублей.")
        await message.answer(text="Сколько хотите вывести?",
                             reply_markup=cancel_inline_menu)
        return
    if user.balance < amount:
        await message.answer("На вашем балансе недостаточно средств...")
        await state.finish()
        return
    if config.BALANCE_LIMIT < amount:
        await message.answer("Технический перерыв, в течении 24х часов вы сможете вывести средства!")
        await state.finish()
        return
    answer_from_qiwi = Payment.send_to_qiwi(user.phone, amount_with_fee)
    try:
        status_transaction = answer_from_qiwi["transaction"]["state"]
    except:
        await bot.send_message(chat_id=config.ADMINS[0],
                               text=f"У {hlink('пользователя', message.from_user.url)} возникла проблема при выводе\n"
                                    f"Ошибка: {answer_from_qiwi['message']}")
        await message.answer("При выводе произошла ошибка, проверьте данные для вывода.\n"
                             "Вывод возможен только на верифицированные счёта!\n"
                             "С Вами свяжется администратор.")
        await state.finish()
        return
    print(status_transaction)
    if status_transaction['code'] == "Accepted":
        await message.answer("Вывод будет выполнен в течении 2 часов.\n"
                             "Вывод возможен только на верифицированные счёта!")
        await user_quick_commands.change_balance(message.from_user.id, -amount)
        config.ADMIN_BALANCE -= amount
        config.BALANCE_LIMIT -= amount
        if user.username:
            username = user.username
        else:
            username = " - "
        await bot.send_message(chat_id=config.MAIN_CHAT_ID,
                               text=f"""❗️Заявка на вывод одобрена   ❗️

К выводу: {amount} монет
Ник получателя: @{username}
id получателя: {user.id}

Спасибо что вы с нами! 🥰
""")
    await state.finish()


def get_soum_to_withdrad(amount: float, fee: float):
    finish_amount = amount * fee
    finish_amount_with_fee = finish_amount * 1.02
    return finish_amount_with_fee
