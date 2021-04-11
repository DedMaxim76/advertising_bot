from aiogram.utils.markdown import hlink

from data import config
from loader import bot
from utils.db_api.quick_commands import user_quick_commands


async def show_top():
    users: list = await user_quick_commands.select_all_users()
    users.sort(key=lambda i: i.num_of_active_referrals, reverse=True)
    top_list = users[:10]
    top_text = "<b>ТОП фармеров активных!</b>\n\n"
    iterator = 1
    for user in top_list:
        user_full_name: str = user.full_name
        user_url = f"tg://user?id={user.id}"
        url = f"{hlink(user_full_name, user_url)}"
        top_text += f"<b>{iterator}</b>. {url} = {user.num_of_active_referrals} уч.\n"
        iterator += 1
    for user in users:
        await bot.send_message(chat_id=user.id,
                               text=top_text)
    await bot.send_message(chat_id=config.MAIN_CHAT_ID,
                           text=top_text)
