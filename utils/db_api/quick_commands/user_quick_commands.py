import random

from asyncpg import UniqueViolationError

from loader import bot
from utils.db_api.db_gino import db
from utils.db_api.schemas.users import User


async def add_user(user_id: int, full_name: str, user_name: str, inviter_code: str):
    try:
        referral_code = str(random.randint(10000000, 99999999))
        user = User(id=user_id,
                    full_name=full_name,
                    username=user_name,
                    inviter_code=inviter_code,
                    referral_code=referral_code)
        await user.create()
    except UniqueViolationError:
        pass


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_users_in_game():
    users = await User.query.where(User.in_game).gino.all()
    return users


async def count_users():
    total = await db.func.count(User.id).gino.scalar()
    return total


async def get_count_of_referrals(user_id):
    inviter = await User.get(user_id)
    if inviter.referral_code is None:
        return 0
    users = await User.query.where(User.inviter_code == inviter.referral_code).gino.all()
    print(users)
    if users is not None:
        total = len(users)
    else:
        total = 0
    return total


async def select_user(user_id: int):
    # user = await User.query.where(User.id == id).gino.first()
    user = await User.get(user_id)
    if not user:
        return None
    return user


async def select_user_by_referral(referral_code: str):
    user = await User.query.where(User.referral_code == referral_code).gino.first()
    if not user:
        return None
    return user


async def change_balance(user_id: int, balance: float):
    user = await User.get(user_id)
    balance_temp = user.balance + balance
    if balance_temp < 0:
        balance_temp = 0
    await user.update(balance=balance_temp).apply()


async def change_phone(user_id: int, phone: str = None):
    user = await User.get(user_id)
    await user.update(phone=phone).apply()


async def change_card(user_id: int, card: str = None):
    user = await User.get(user_id)
    await user.update(card=card).apply()


async def change_referral_code(user_id: int, referral_code: str):
    user = await User.get(user_id)
    await user.update(referral_code=referral_code).apply()


async def change_inviter_code(user_id: int, inviter_code: str):
    user = await User.get(user_id)
    await user.update(inviter_code=inviter_code).apply()


async def add_acitve_refferal(user_id: int):
    user = await User.get(user_id)
    await user.update(num_of_active_referrals=user.num_of_active_referrals + 1).apply()
    if user.num_of_active_referrals % 10 == float(0):
        await bot.send_message(chat_id=user_id, text="Вам начислена 1 монета! За каждые 10+ активных")
        await change_balance(user_id, 1)


async def del_acitve_refferal(user_id: int):
    user = await User.get(user_id)
    num_of_active_referrals = user.num_of_active_referrals - 1
    if num_of_active_referrals < 0:
        num_of_active_referrals = 0
    await user.update(num_of_active_referrals=num_of_active_referrals).apply()


async def add_passive_refferal(user_id: int):
    user = await User.get(user_id)
    await user.update(num_of_passive_referrals=user.num_of_passive_referrals + 1).apply()
    if user.num_of_passive_referrals % 100 == float(0):
        await bot.send_message(chat_id=user_id, text="Вам начислена 1 монета! За каждые 100+ ожидаемых")
        await change_balance(user_id, 1)


async def del_passive_refferal(user_id: int):
    user = await User.get(user_id)
    num_of_passive_referrals = user.num_of_passive_referrals - 1
    if num_of_passive_referrals < 0:
        num_of_passive_referrals = 0
    await user.update(num_of_passive_referrals=num_of_passive_referrals).apply()


async def add_bonus_referrals(user_id: int):
    user = await User.get(user_id)
    await user.update(bonus_referrals=user.bonus_referrals + 1).apply()


async def del_all_bonus_referrals(user_id: int):
    user = await User.get(user_id)
    await user.update(bonus_referrals=0).apply()


async def add_to_game(user_id: int):
    user = await User.get(user_id)
    if user:
        await user.update(in_game=True).apply()


async def ban_user(user_id: int):
    user = await User.get(user_id)
    if user:
        await user.update(banned=True).apply()


async def unban_user(user_id: int):
    user = await User.get(user_id)
    if user:
        await user.update(banned=False).apply()
