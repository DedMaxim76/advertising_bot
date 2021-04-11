from loader import bot
from utils.db_api.quick_commands import user_quick_commands


async def withdraw_weekly_bonus():
    users: dict = await user_quick_commands.select_all_users()
    for user in users:
        if user.bonus_referrals == 0:
            continue
        bonus = user.bonus_referrals * 0.1
        await user_quick_commands.change_balance(user.id, bonus)
        await user_quick_commands.del_all_bonus_referrals(user.id)
        await bot.send_message(chat_id=user.id,
                               text=f"Вам пришли бонусные {bonus} монет,\n"
                                    f"за {user.bonus_referrals} активных рефералов.")