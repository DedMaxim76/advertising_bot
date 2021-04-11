import re

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.markdown import hlink

from data import config
from filters import IsChatMember, IsAdmin
from handlers.users.admin_handlers.admin_commands import get_admin_commands
from keyboards.default.start_keyboard import start_menu, start_menu_admin
from loader import dp, bot
from utils.db_api.quick_commands import user_quick_commands
from utils.db_api.schemas.users import User


@dp.message_handler(CommandStart(deep_link=re.compile(r"\d+")), IsChatMember())
async def bot_start_deeplink_member(message: types.Message):
    deep_link_args = message.get_args()
    inviter_code = deep_link_args
    user: User = await user_quick_commands.select_user(message.from_user.id)
    if user:
        if user.inviter_code == inviter_code:
            await message.answer("<b>Добро пожаловать!</b>", reply_markup=start_menu)
            return
        else:
            await message.answer("<b>Вы уже зарегистрированы!</b>")
            return
    inviter: User = await user_quick_commands.select_user_by_referral(inviter_code)
    if not inviter:
        await message.answer("Неверная ссылка!")
        return
    await user_quick_commands.add_user(user_id=message.from_user.id,
                                       full_name=message.from_user.first_name,
                                       user_name=message.from_user.username,
                                       inviter_code=inviter_code)
    await message.answer("<b>Добро пожаловать!</b>", reply_markup=start_menu)
    if inviter_code == config.INVITER_CODE:
        return
    await user_quick_commands.add_passive_refferal(inviter.id)
    if inviter.inviter_code == config.INVITER_CODE:
        return
    inviter_of_inviter: User = await user_quick_commands.select_user_by_referral(inviter.inviter_code)
    await user_quick_commands.add_bonus_referrals(inviter_of_inviter.id)                            # bonus system!!!!!!
    if inviter.num_of_active_referrals == 0 and inviter.num_of_passive_referrals == 0:
        await user_quick_commands.del_passive_refferal(inviter_of_inviter.id)
        await user_quick_commands.add_acitve_refferal(inviter_of_inviter.id)
        await bot.send_message(chat_id=inviter_of_inviter.id,
                               text="<b>Вам начислена 1 монета! За активного реферала.</b>")
        await user_quick_commands.change_balance(inviter_of_inviter.id, 1)
        if inviter_of_inviter.inviter_code == config.INVITER_CODE:
            return
        inviter_of_inviter_of_inviter: User = await user_quick_commands.select_user_by_referral(
            inviter_of_inviter.inviter_code)
        await bot.send_message(chat_id=inviter_of_inviter_of_inviter.id,
                               text="<b>Вам начислена 1 монета! "
                                    "За активного реферала у вашего реферала.</b>")
        await user_quick_commands.change_balance(inviter_of_inviter_of_inviter.id, 1)
        

@dp.message_handler(CommandStart(deep_link=re.compile(r"\d+")))
async def bot_start_deeplink_not_member(message: types.Message):
    deep_link_args = message.get_args()
    print(deep_link_args)
    await message.answer(f"Чтоб пользоваться ботом, вы должны быть подписаны на канал "
                         f"{hlink('Vital Change', config.MAIN_CHANNEL_URL)}")


@dp.message_handler(CommandStart(), IsAdmin())
async def bot_start_without_link(message: types.Message):
    await user_quick_commands.add_user(user_id=message.from_user.id,
                                       full_name=message.from_user.first_name,
                                       user_name=message.from_user.username,
                                       inviter_code=config.INVITER_CODE)
    await message.answer(f"<b>Добро пожаловать, администратор!</b>\n",
                         reply_markup=start_menu_admin)


@dp.message_handler(CommandStart())
async def bot_start_without_link(message: types.Message):
    user: User = await user_quick_commands.select_user(message.from_user.id)
    if user:
        await message.answer("<b>Добро пожаловать!</b>", reply_markup=start_menu)
        return
    await message.answer(f"Сюда можно попасть только по приглашению…")


@dp.message_handler(text="👨🏻‍💻 Админ панель")
async def send_admin_commands(message: types.Message):
    await get_admin_commands(message)
