from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink

from data import config
from handlers.users.balance_handlers.withdraw_qiwi import get_soum_to_withdrad, Max_Withdraw, Min_Withdraw, Card_Fee
from keyboards.inline.callback_datas import payment_method_callback, accept_card_callback, cancel_callback
from keyboards.inline.withdraw_inline_menu import accept_card_inline_menu, cancel_inline_menu
from loader import dp, bot
from utils.db_api.quick_commands import user_quick_commands
from utils.db_api.schemas.users import User
from utils.misc.qiwi import Payment


@dp.callback_query_handler(payment_method_callback.filter(method="card"))
async def withdraw_card(call: CallbackQuery, state: FSMContext):
    user: User = await user_quick_commands.select_user(call.from_user.id)
    await call.message.delete()
    await call.message.answer("Комиссия сервиса на вывод 2% + 50 рублей.")
    if user.card:
        secret_card = user.card[12:]
        await call.message.answer(text=f"Осуществить вывод на вашу карту **** **** **** {secret_card}?",
                                  reply_markup=accept_card_inline_menu)
        await state.set_state("waiting_for_accept_card")
    else:
        await call.message.answer("<b>Введите номер карты</b>:\n"
                                  "<i>*Карта сохраниться за вашим аккаунтом.</i>",
                                  reply_markup=cancel_inline_menu)
        await state.set_state("waiting_for_card")


@dp.callback_query_handler(cancel_callback.filter(withdraw_method="pass"), state="*")
async def cancel_withdraw(call: CallbackQuery, state: FSMContext):
    await call.answer("Вы отменили вывод средств.")
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(accept_card_callback.filter(choice="yes"), state="waiting_for_accept_card")
async def withdraw_card_accept(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Введите суму вывода:",
                              reply_markup=cancel_inline_menu)
    await state.set_state("waiting_for_soum_to_withdraw")


@dp.callback_query_handler(accept_card_callback.filter(choice="no"), state="waiting_for_accept_card")
async def withdraw_card_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await user_quick_commands.change_card(call.from_user.id)
    await call.message.answer(text="Введите номер карты на которую хотите сделать вывод:",
                              reply_markup=cancel_inline_menu)
    await state.set_state("waiting_for_card")


@dp.message_handler(state="waiting_for_card")
async def withdraw_card(message: types.Message, state: FSMContext):
    card = message.text.lower()
    if not card.isdigit() or len(card) != 16:
        await message.answer("Ошибка при проверке карты....")
        await message.answer("Введите номер карты на которую хотите сделать вывод:\n"
                             "Карта сохраниться за вашим аккаунтом.",
                             reply_markup=cancel_inline_menu)
        return
    await user_quick_commands.change_card(message.from_user.id, card)
    await message.answer(text="Сколько хотите вывести? ",
                         reply_markup=cancel_inline_menu)
    await state.set_state("waiting_for_soum_to_withdraw")


@dp.message_handler(state="waiting_for_soum_to_withdraw")
async def withdraw_card_send(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Вы ввели не число, попробуйте снова.")
        await message.answer(text="Сколько хотите вывести? ",
                             reply_markup=cancel_inline_menu)
        return
    user: User = await user_quick_commands.select_user(message.from_user.id)
    amount = float(message.text)
    amount_with_fee = (amount - Card_Fee) * 0.98
    if user.balance < amount:
        await message.answer("На вашем балансе недостаточно средств...")
        await state.finish()
        return
    if amount > Max_Withdraw or amount < Min_Withdraw + Card_Fee:
        await message.answer("Минимальная сума вывода 60 рублей.\n"
                             "Максимальная 1000 рублей.")
        await message.answer(text="Сколько хотите вывести? ",
                             reply_markup=cancel_inline_menu)
        return
    if config.BALANCE_LIMIT < amount:
        await message.answer("Технический перерыв, в течении 24х часов вы сможете вывести средства!")
        await state.finish()
        return
    prv_id = Payment.get_card_system(user.card)
    payment_data = {'sum': amount_with_fee,
                    'to_card': user.card,
                    'prv_id': prv_id}
    answer_from_qiwi = Payment.send_to_card(payment_data)
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
    if status_transaction['code'] == "Accepted":
        await message.answer("Вывод будет выполнен в течении 2 часов.\n"
                             "Комиссия Qiwi 2% + 50 рублей.\n"
                             "Вывод возможен только на верифицированные счёта!")
        await user_quick_commands.change_balance(message.from_user.id, -amount)
        config.BALANCE_LIMIT -= amount
        config.ADMIN_BALANCE -= amount
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
